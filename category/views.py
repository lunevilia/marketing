from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import CategoryForm
import re

# Create your views here.
def show_category(request): #게시판 보이게 하기 및 작성하기
    show_all = Category.objects.all()
    if request.method == 'POST':
        if request.user.is_superuser:
            form = CategoryForm(request.POST)
            if form.is_valid():
                num_important = int(form.cleaned_data.get("important"))

                #elif의 변경을 적용시키기 위해서 일단 False
                form_wait = form.save(commit=False)

                #생성시에 적용하도록 (form wait는 이 함수를 통해서 save를 한다)
                create_then_order(show_all, num_important, form_wait)

                return redirect('/category/')
        else:
            return redirect('/category/')
    else:
        form = CategoryForm()
        show_all = Category.objects.all()

    return render(request, 'category_detail.html', {'form':form, 'show_all':show_all})

def mod_category(request, id): #게시판 이름 바꾸기
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
    #중복되는 숫자가 있으면 밀려나게 만들기
    last = obj.count()
    if obj.filter(important=create_obj_important).exists():
        for i in range(last, create_obj_important-1, -1):
            change_important = obj.get(important=i)
            change_important.important = i + 1
            change_important.save()
        waitform.save()

    #만약 맨 마지막에 들어갈 숫자 보다 클 경우 맨 마지막 숫자로 넣기
    elif create_obj_important > last:
        waitform.important = last + 1
        waitform.save()