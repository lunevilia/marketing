from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from account.models import Profile
from category.models import Category
from django.contrib.auth.models import User
# Create your views here.

def selectform(request, board="자유게시판"): #작성하기 및 전체 글 보여주기
    getCategory = get_object_or_404(Category, board_name=board) #board는 url로 통해서 category에 선택하는 게시판을 클릭하면 board가 들어와짐
    if request.method == 'POST':
        form = FormTest(request.POST)
        imageform = ImageTest(request.POST, request.FILES)
        filesform = FilesTest(request.POST, request.FILES)
        
        if form.is_valid():
            getProfile = Profile.objects.get(user__username=request.user) #안됬는데 보니깐 슈퍼유저는 Profile이 안만들어져서 찾지를 못하는 것이였음
            a = form.save(commit=False)
            a.author = getProfile
            a.category = getCategory #글을 작성할때 category를 자동으로 작성할 수 있도록 설정
            a.save()

            if imageform.is_valid():
                image_list = request.FILES.getlist('image')
                for item in image_list: 
                    image = Image.objects.create(post=a, image=item)
                    image.save()

            if filesform.is_valid():
                files_list = request.FILES.getlist('files')
                for item in files_list: 
                    files = Files.objects.create(post=a, files=item)
                    files.save()
            return redirect('/board/'+str(board))
    else:
        form = FormTest()
        imageform = ImageTest()
        filesform = FilesTest()

        if board:
            getForm = Defaultform.objects.filter(category__board_name=board)
        else:
            getForm = Defaultform.objects.all()

    return render(request, 'formtest.html', {'form':form, 'imageform':imageform, 'filesform':filesform, 'getForm':getForm, 'board_name':board,})

def shw_form(request, board, id): #글의 자세한 내용 보여주기
    detail_getForm = get_object_or_404(Defaultform, id=id)
    image_getForm = Image.objects.filter(post=detail_getForm)
    files_getForm = Files.objects.filter(post=detail_getForm)

    return render(request, 'form_detail.html', {'detail_getForm':detail_getForm, })

def mod_form(request, board, id): #글 수정하기
    mod_getForm = get_object_or_404(Defaultform, id=id)

    if request.method == 'POST':
        form = FormTest(request.POST, instance=mod_getForm)
        
        if form.is_valid():
            a = form.save()

            if request.POST.get("image_modify"): #그전에 있던 녀석들을 삭제! 추가해야됨
                pre_image_delete = Image.objects.filter(post=mod_getForm)
                pre_image_delete.delete()
                image_list = request.FILES.getlist('image')

                for item in image_list: 
                    image = Image.objects.create(post=mod_getForm, image=item)
                    image.save()

            if request.POST.get("files_modify"):
                pre_files_delete = Files.objects.filter(post=mod_getForm)
                pre_files_delete.delete()
                files_list = request.FILES.getlist('files')

                for item in files_list: 
                    files = Files.objects.create(post=mod_getForm, files=item)
                    files.save()

            return redirect('/board/'+str(board)+'/'+str(id))
    else:
        form = FormTest(instance=mod_getForm)
        # imageform = ImageTest(instance=mod_getImage)
        # filesform = FilesTest(instance=mod_getFile)

    return render(request, 'form_mod.html', {'id':id, 'form':form, 'mod_getForm':mod_getForm})

def del_form(request, board, id): #글 삭제하기
    post_instance = Defaultform.objects.get(id=id)
    post_instance.delete()
    return redirect('/board/'+str(board))

def ajax_mod_form(request, board, id): #글 수정하기
    mod_getForm = get_object_or_404(Defaultform, id=id)
    mod_getImage = get_object_or_404(Image, post=mod_getForm)
    mod_getFile = get_object_or_404(Files, post=mod_getForm)

    if request.method == 'POST':
        form = FormTest(request.POST, instance=mod_getForm)
        imageform = ImageTest(request.FILES, instance=mod_getImage)
        filesform = FilesTest(request.FILES, instance=mod_getFile)
        if form.is_valid():
            a = form.save()

            if imageform.is_valid():
                image_list = request.FILES.getlist('image')
                for item in image_list: 
                    image = Image.objects.create(post=a, image=item)
                    image.save()

            if filesform.is_valid():
                files_list = request.FILES.getlist('files')
                for item in files_list: 
                    files = Files.objects.create(post=a, files=item)
                    files.save()
                    
            return redirect('/board/'+str(board)+'/'+str(id))
    else:
        form = FormTest(instance=mod_getForm)
        imageform = ImageTest(instance=mod_getImage)
        filesform = FilesTest(instance=mod_getFile)

    return render(request, 'form_mod.html', {'id':id, 'form':form, 'mod_getForm':mod_getForm})