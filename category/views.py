from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import CategoryForm
import re
from django.contrib import messages


def show_category(request): #게시판 보이게 하기 및 작성하기
    show_all = Category.objects.all()
    # GET과 POST 둘 다 현재 까지 작성한 모든 게시판 정보를 가져와서 사용하기 위해 show_all을 작성
        #show_all : 모든 게시판 정보의 query_set

    if request.method == 'POST':
        if request.user.is_superuser:
        # 만약 운영자일 경우만 해당 POST를 할 수 있도록 설정
            form = CategoryForm(request.POST)
            # POST의 모든 정보를 받아서 해당 정보를 CategoryForm에 넣어 form이라는 객체를 생성
                # form : POST 정보를 가진 form 정보
            if form.is_valid():
            # 만약 해당 POST들이 form의 규격에 맞을 경우에만 작업 처리
                num_important = int(form.cleaned_data.get("important"))
                # POST에서 받은 important라는 데이터 값을 num_important에 integer로 형 변환
                    # num_important : important 값의 정수형
                    # num_important : Category 레코드를 만들때, 같은 important(순위)가 있을 경우에 순위 같은 것을 다음 수로 밀기 위해서 나중에 사용

                form_wait = form.save(commit=False)
                # 같은 important(순위)가 있는지 확인하고 저장하기 위해서 저장을 보류
                    #form_wait : 모든 POST 데이터가 들어가 있고 레코드로 넣지 않은 상태

                create_then_order(show_all, num_important, form_wait)
                # 생성시에 적용하도록 (form wait는 이 함수를 통해서 save를 한다)
                    # create_then_order(모든 게시판 개수와 다른 게시판의 정보를 알기 위해서 삽입, 넣고 싶은 순위의 정보, 아직 저장만 하지 않은 완전체의 상태)
                return redirect('/category/')
            else:
                messages.info(request, '생성 중 오류가 났습니다!')
                # POST들 중 form 규격에 맞지 않을 경우 오류가 났다고 알림!
                return redirect('/category/')
        else:
        # 만약 운영자가 아닐 경우 해당 작업을 못하도록 그냥 원래 있던 곳으로 보내기
            return redirect('/category/')
    else:
    # POST가 아닌 GET일 경우
        form = CategoryForm()
        # Category의 정보로 만들어진 form을 html에 뿌려주기 위해서 form이라는 객체를 생성
    return render(request, 'category_detail.html', {'form':form, 'show_all':show_all})

def mod_category(request, id): #게시판 정보 바꾸기
    mod_getForm = get_object_or_404(Category, id=id)
    current_important = mod_getForm.important #위에 있는 값들의 숫자를 1개씩 줄이기 위해 시작의 위치를 파악
    show_all = Category.objects.all()
    last = show_all.count()

    if request.user.is_superuser:
        if request.method == 'POST':
            form = CategoryForm(request.POST, instance=mod_getForm)
            if form.is_valid():
                after_important = int(form.cleaned_data.get("important"))
                a = form.save(False)

                ### 게시판 순서 옮기기(교환하기) 함수로 만들지 않은 이유는 나중에 까먹을 것 같아서... ###
                if show_all.filter(important=after_important).exists():
                    #위로 옮겼을 경우
                    if current_important > after_important:
                        for i in range(current_important-1, after_important-1, -1):
                            change_important = show_all.get(important=i)
                            change_important.important = i + 1
                            change_important.save()
                        a.save()
                    #아래로 옮겼을 경우
                    elif current_important < after_important:
                        for i in range(current_important+1, after_important+1):
                            change_important = show_all.get(important=i)
                            change_important.important = i - 1
                            change_important.save()
                        a.save()
                    else:
                        a.save()

                #만약 맨 마지막에 들어갈 숫자 보다 클 경우 맨 마지막 숫자로 넣기
                elif after_important > last:
                    for i in range(current_important+1, last+1):
                        change_important = show_all.get(important=i)
                        change_important.important = i - 1
                        change_important.save()
                    a.important = last
                    a.save()

                return redirect('/category/')

            #form에 문제가 생길 경우!
            else:
                messages.info(request, '변경 중 오류가 났습니다!')
                return redirect('/category/')
        else:
            form = CategoryForm(instance=mod_getForm)
    else:
        return redirect('/category/')

def delete_category(request, id): #게시판 삭제하기
    show_all = Category.objects.all()
    if request.user.is_superuser:
        post_instance = Category.objects.get(id=id)
        delete_important = post_instance.important

        #하나가 삭제되면 그 위의 숫자들은 하나씩 줄음
        delete_then_order(show_all, delete_important)
        
        post_instance.delete()

        return redirect('/category/')
    else:
        return redirect('/category/')

#하나가 삭제되면 그 위의 숫자들은 하나씩 줄음
def delete_then_order(obj, delete_obj_important):
    if obj.filter(important=delete_obj_important+1).exists():
            last = obj.count()
            for i in range(delete_obj_important+1, last+1):
                change_important = obj.get(important=i)
                change_important.important = i - 1
                change_important.save()

def create_then_order(obj, create_obj_important, waitform):    
    last = obj.count()
    # 게시판 테이블의 모든 개수를 알기 위함

    # 중복되는 숫자가 있으면 밀려나게 만들기
    if obj.filter(important=create_obj_important).exists():
    # 게시판 테이블 중 생성하고 싶은 important(순위)와 동일한 것이 존재하는지 확인
        for i in range(last, create_obj_important-1, -1):
        # 있을 경우 마지막 부분에 있는 레코드 부터 넣고 싶은 important(순위)까지 하나씩 important(순위)를 늘리기
            change_important = obj.get(important=i)
            change_important.important = i + 1
            change_important.save()
        waitform.save()
        # 모든 것을 마친뒤에 해당 form 데이터를 저장

    #만약 맨 마지막에 들어갈 숫자 보다 클 경우 맨 마지막 숫자로 넣기
    elif create_obj_important > last:
        waitform.important = last + 1
        waitform.save()