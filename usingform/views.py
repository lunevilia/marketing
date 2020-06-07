from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from account.models import Profile, Commentalert
from category.models import Category
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
# Create your views here.

def selectform(request, board="자유게시판"): #작성하기 및 전체 글 보여주기
    if request.session.get('page'): #저장된 위치 삭제
        del request.session['page']
        
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
    #session 저장해서 그 좋아요 부분이랑 나누기 위해서 적용
    page = request.session.get('page', False)

    #글 내용 보여주기
    detail_getForm = get_object_or_404(Defaultform, id=id)
    #댓글 보여주기
    detail_getComment = Comment.objects.filter(main_post=detail_getForm, post__isnull=True)
    commentform = CommentTest()
    return render(request, 'form_detail.html', {'detail_getForm':detail_getForm, 'commentform':commentform, 'detail_getComment':detail_getComment, 'page':page,})

def mod_form(request, board, id): #글 수정하기
    mod_getForm = get_object_or_404(Defaultform, id=id)

    if request.method == 'POST':
        form = FormTest(request.POST, instance=mod_getForm)
        
        if form.is_valid():
            a = form.save()

            if request.POST.get("image_modify"):
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

def del_form(request, board, id): #글 삭제하기
    post_instance = Defaultform.objects.get(id=id)
    if post_instance.author.user.username == request.user.username:
        post_instance.delete()
    return redirect('/board/'+str(board))

#댓글 생성
def comment_write(request, board, id):
    if request.method == 'POST':
        main_post = Defaultform.objects.get(id=id)
        # if comment_id:
        #     post = Comment.objects.get(id=comment_id)
        #답글을 클릭하면 option request.post로 option id번호 주기
        commentform = CommentTest(request.POST)
        if commentform.is_valid():
            getProfile = Profile.objects.get(user__username=request.user) #안됬는데 보니깐 슈퍼유저는 Profile이 안만들어져서 찾지를 못하는 것이였음
            a = commentform.save(commit=False)
            a.author = getProfile
            a.main_post = main_post
            a.save()

            #알람 차단한 사람은 알려주지 않고, 알람 차단하지 않은 사람은 알려주기
            #내가 내 글에 댓글을 작성했을 경우!
            if not (main_post.author.user.username == request.user.username) and not (Donotalert.objects.filter(profile=main_post.author, board=main_post).exists()):
                comment_a = Commentalert.objects.get(profile=main_post.author)
                comment_a.recent = comment_a.recent+1
                comment_a.save()

                body = commentform.cleaned_data['body']
                #내용과 id를 저장하기
                Commentalertcontent.objects.create(board=main_post, sender_name=getProfile.Name, profile_name=main_post.author.Name, content=body)
            
            return redirect('/board/'+str(board)+'/'+str(id))

#댓글 삭제
def comment_del(request, board, id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.author.user.username == request.user.username:
        comment.delete()
    return redirect('/board/'+str(board)+"/"+str(id))

#대댓글 생성
def recomment_write(request, board, id, comment_id):
    if request.method == 'POST':
        main_post = Defaultform.objects.get(id=id)
        post = Comment.objects.get(id=comment_id)
        #답글을 클릭하면 option request.post로 option id번호 주기
        commentform = CommentTest(request.POST)
        if commentform.is_valid():
            getProfile = Profile.objects.get(user__username=request.user) #안됬는데 보니깐 슈퍼유저는 Profile이 안만들어져서 찾지를 못하는 것이였음
            a = commentform.save(commit=False)
            a.author = getProfile
            a.main_post = main_post
            a.post = post
            a.save()

            #알람 차단한 사람은 알려주지 않고, 알람 차단하지 않은 사람은 알려주기
            if not (post.author.user.username == request.user.username) and not (Donotalert.objects.filter(profile=post.author, board=main_post).exists()):
                comment_a = Commentalert.objects.get(profile=post.author)
                comment_a.recent = comment_a.recent+1
                comment_a.save()

                body = commentform.cleaned_data['body']
                #내용과 id를 저장하기
                Commentalertcontent.objects.create(board=main_post, sender_name=getProfile.Name, profile_name=post.author.Name, content=str("(답글) ")+body)

            return redirect('/board/'+str(board)+'/'+str(id))

#댓글 좋아요
def ajax_comment_like(request, comment_id):
    if request.is_ajax():
        comment = Comment.objects.get(id=comment_id)
        getProfile = Profile.objects.get(user__username=request.user) #안됬는데 보니깐 슈퍼유저는 Profile이 안만들어져서 찾지를 못하는 것이였음

        #있을 경우 삭제
        try:
            a = CommentLike.objects.get(post=comment, author=getProfile)
            a.delete()
            like_state = True #없어졌으니깐 좋아요를 누를 수 있음
        #없을 경우 생성
        except:
            CommentLike.objects.create(post=comment, author=getProfile)
            like_state = False #생기니깐 좋아요 취소 누를 수 있음

        count_like = CommentLike.objects.filter(post=comment).count()
        return HttpResponse(json.dumps({'count_like':str(count_like), 'like_state':like_state,}), 'application/json')

#게시글 좋아요
def ajax_board_like(request, id):
    if request.is_ajax():
        board = Defaultform.objects.get(id=id)
        getProfile = Profile.objects.get(user__username=request.user) #안됬는데 보니깐 슈퍼유저는 Profile이 안만들어져서 찾지를 못하는 것이였음

        #있을 경우 삭제
        try:
            a = Like.objects.get(post=board, author=getProfile)
            a.delete()
            like_state = True #없어졌으니깐 좋아요를 누를 수 있음
        #없을 경우 생성
        except:
            Like.objects.create(post=board, author=getProfile)
            like_state = False #생기니깐 좋아요 취소 누를 수 있음

        board_like = Like.objects.filter(post=board).count()
        return HttpResponse(json.dumps({'board_like':str(board_like), 'like_state':like_state,}), 'application/json')

#게시글 즐겨찾기
def ajax_board_favorite(request, id):
    if request.is_ajax():
        board = Defaultform.objects.get(id=id)
        getProfile = Profile.objects.get(user__username=request.user) #안됬는데 보니깐 슈퍼유저는 Profile이 안만들어져서 찾지를 못하는 것이였음

        #있을 경우 삭제
        try:
            a = Favorite.objects.get(post=board, author=getProfile)
            a.delete()
            like_state = True #없어졌으니깐 좋아요를 누를 수 있음
        #없을 경우 생성
        except:
            Favorite.objects.create(post=board, author=getProfile)
            like_state = False #생기니깐 좋아요 취소 누를 수 있음

        board_favorite = Favorite.objects.filter(post=board).count()
        return HttpResponse(json.dumps({'board_favorite':str(board_favorite), 'like_state':like_state,}), 'application/json')

#알람 차단하기
def ajax_donot_alert(request, id):
    if request.is_ajax():
        board = Defaultform.objects.get(id=id)
        getProfile = Profile.objects.get(user__username=request.user) #안됬는데 보니깐 슈퍼유저는 Profile이 안만들어져서 찾지를 못하는 것이였음

        #있을 경우 삭제
        try:
            a = Donotalert.objects.get(board=board, profile=getProfile)
            a.delete()
            like_state = True #없어졌으니깐 좋아요를 누를 수 있음
        #없을 경우 생성
        except:
            Donotalert.objects.create(board=board, profile=getProfile)
            like_state = False #생기니깐 좋아요 취소 누를 수 있음

        board_donotalert = Donotalert.objects.filter(board=board).count()
        return HttpResponse(json.dumps({'board_donotalert':str(board_donotalert), 'like_state':like_state,}), 'application/json')
