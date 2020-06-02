from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from category.models import Category
# Create your views here.

def selectform(request, board="자유게시판"): #작성하기 및 전체 글 보여주기
    getCategory = get_object_or_404(Category, board_name=board) #board는 url로 통해서 category에 선택하는 게시판을 클릭하면 board가 들어와짐
    if request.method == 'POST':
        form = FormTest(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.category = getCategory #글을 작성할때 category를 자동으로 작성할 수 있도록 설정
            a.save()
            return redirect('/board/'+str(board))
    else:
        form = FormTest()
        if board:
            getForm = Defaultform.objects.filter(category__board_name=board)
        else:
            getForm = Defaultform.objects.all()

    return render(request, 'formtest.html', {'form':form, 'getForm':getForm, 'board_name':board,})

def shw_form(request, board, id): #글의 자세한 내용 보여주기
    detail_getForm = get_object_or_404(Defaultform, id=id)
    return render(request, 'form_detail.html', {'detail_getForm':detail_getForm, })

def mod_form(request, board, id): #글 수정하기
    mod_getForm = get_object_or_404(Defaultform, id=id)

    if request.method == 'POST':
        form = FormTest(request.POST, instance=mod_getForm)
        if form.is_valid():
            a = form.save()
            return redirect('/board/'+str(board)+'/'+str(id))
    else:
        form = FormTest(instance=mod_getForm)

    return render(request, 'form_mod.html', {'id':id, 'form':form, 'mod_getForm':mod_getForm})

def del_form(request, board, id): #글 삭제하기
    post_instance = Defaultform.objects.get(id=id)
    post_instance.delete()
    return redirect('/board/'+str(board))