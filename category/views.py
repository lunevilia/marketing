from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import CategoryForm

# Create your views here.
def show_category(request): #게시판 보이게 하기 및 작성하기
    show_all = Category.objects.all()
    if request.method == 'POST':
        if request.user.is_superuser:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/category/')
        else:
            return redirect('/category/')
    else:
        form = CategoryForm()
        show_all = Category.objects.all()

    return render(request, 'category_detail.html', {'form':form, 'show_all':show_all})

def mod_category(request, id): #게시판 이름 바꾸기
    mod_getForm = get_object_or_404(Category, id=id)
    if request.user.is_superuser:
        if request.method == 'POST':
            form = CategoryForm(request.POST, instance=mod_getForm)
            if form.is_valid():
                a = form.save()
                return redirect('/category/')
        else:
            form = CategoryForm(instance=mod_getForm)
    else:
        return redirect('/category/')

def delete_category(request, id): #게시판 삭제하기
    if request.user.is_superuser:
        post_instance = Category.objects.get(id=id)
        post_instance.delete()
        return redirect('/category/')
    else:
        return redirect('/category/')

