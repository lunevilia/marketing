from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from usingform.forms import ImportantTest
from usingform.models import Important_board
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
import json
from usingform.models import Commentalertcontent
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#Email 전송
from django.core.mail import EmailMessage

import random
import string

def login(request):
    if request.method == "POST":
        if request.is_ajax():
            username = request.POST.get("login_username")
            password = request.POST.get("login_password")
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                _next = request.POST.get('next', '/')
                return HttpResponse(json.dumps({'login_error':None, '_next':_next}), 'application/json')
            else:
                login_error = "아이디 혹은 비밀번호를 잘못 입력하셨습니다!"
                return HttpResponse(json.dumps({'login_error':login_error}), 'application/json')

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if request.POST["password1"]==request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST.get("username_id"),
                password=request.POST.get("password1")
            )
            if form.is_valid():
                profile = Profile(
                    user=user,
                    Name=form.cleaned_data.get('Name'),
                    Image=form.cleaned_data.get('Image'), #이미지 및 파일을 저장하려면 html에 있는 form에 enctype="multipart/form-data" 추가
                    Email=form.cleaned_data.get('Email'),
                )
                profile.save()
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, '회원가입 중 비정상 적인 방법으로 접근했습니다.\n다시 회원가입해주세요!')
                return redirect('/')
        else:
            error = "비밀번호를 다시 확인해주세요!"
    else:
        if request.user.is_authenticated:
            return redirect('/account/profile')

        error = ""
        form = SignupForm()

    return render(request, "signup.html", {"form":form, "error":error,})

#랜덤 비밀번호 제조
def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

#비밀번호 찾기
def find_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        
        try:
            user = User.objects.get(username=username)
            
            if user.profile.Email == email:
                send_message_title = "Readly의 임시 비밀번호입니다!"
                user_email = email
                
                #임시 비밀번호로 수정
                password = randomString()
                user.set_password(password)
                user.save()

                send_message_body = "회원님의 비밀번호는 '" + str(password) + "'의 임시 비밀번호로 변경되었습니다!"

                email_send = EmailMessage(send_message_title, send_message_body, to=[user_email])
                messages.info(request, '입력하신 이메일로 임시 비밀번호를 전송했습니다!')
                try:
                    email_send.send()
                except:
                    messages.info(request, '유효하지 않은 이메일로 회원가입 하셔서\n이메일 전송이 불가능 합니다!')
                    return redirect('/account/find_password')
        except:
            messages.info(request, '입력하신 회원 정보가 없습니다!')
        return redirect('/account/find_password')
    else:
        return render(request, "find_password.html")

#회원삭제
@login_required(login_url='/')
def del_user(request):
    user = User.objects.get(username=request.user)
    user.delete()
    return redirect('/')

#회원정보 보기 및 수정하기
@login_required(login_url='/')
def profile(request):
    profile_information = Profile.objects.get(user__username=request.user)
    #수정하기
    if request.method == "POST":
        profile_form = ModifyForm(request.POST, request.FILES, instance=profile_information)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('/account/profile')
        else:
            messages.info(request, '비정상적인 수정 방법입니다!\n다시 수정해주세요!')
            return redirect('/account/profile')
    else:
        profile_form = ModifyForm(instance=profile_information)
    return render(request, "profile.html", {"profile_form":profile_form})

@login_required(login_url='/')
def like_board(request):
    request.session['page'] = 'like'
    return render(request, "like_page.html", )

@login_required(login_url='/')
def favorite_board(request):
    request.session['page'] = 'favorite'
    return render(request, "favorite_page.html", )

@login_required(login_url='/')
def donotalert_board(request):
    request.session['page'] = 'donotalert'
    return render(request, "alert_page.html", )

@login_required(login_url='/')
def alert_board(request):
    request.session['page'] = 'alert_board'
    return render(request, "alert.html", )


#중요 게시판 생성
@login_required(login_url='/')
def important_board(request):
    if request.user.is_superuser:
        _board = Important_board.objects.all()
        if request.method == 'POST':
            form = ImportantTest(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/account/important_board')
            else:
                messages.info(request, '생성 중 오류가 났습니다!')
                return redirect('/account/important_board')
        else:
            form = ImportantTest()
        return render(request, "important_page.html", {"form":form, "board":_board,})
    else:
        return redirect('/account/profile')

#중요 게시판 삭제
@login_required(login_url='/')
def del_important_board(request, important_id):
    if request.user.is_superuser:
        del_important = get_object_or_404(Important_board, id=important_id)
        del_important.delete()
        return redirect("/account/important_board/")
    else:
        return redirect('/account/profile')

#중요 게시판 수정
@login_required(login_url='/')
def mod_important_board(request, important_id):
    if request.user.is_superuser:
        mod_board = get_object_or_404(Important_board, id=important_id)
        if request.method == 'POST':
            form = ImportantTest(request.POST, instance=mod_board)
            if form.is_valid():
                form.save()
                return redirect('/account/important_board')
            else:
                messages.info(request, '수정 중 오류가 났습니다!')
                return redirect('/account/important_board')
        else:
            form = ImportantTest(instance=mod_board)
        return render(request, "mod_important_page.html", {"form":form, "mod_board":mod_board,})
    else:
        return redirect('/account/profile')


#중복확인하는 ajax용 함수 만들기 (닉네임, 아이디, 이메일)
def ajax(request, value, region):
    if request.is_ajax():
        if region == "username":
            check = User.objects.filter(username=value).exists()
        elif region == "nickname":
            check = Profile.objects.filter(Name=value).exists()
        elif region == "email":
            check = Profile.objects.filter(Email=value).exists()
        else:
            check = False

        return HttpResponse(json.dumps({'check':check}), 'application/json')

#알람이 되는 ajax!
@login_required(login_url='/')
def notice_ajax(request): 
    if request.is_ajax():
        getProfile = Profile.objects.get(user__username=request.user)
        comment_a = Commentalert.objects.get(profile=getProfile)

        #가져올 개수
        how_many_filter = comment_a.recent - getProfile.alert

        getProfile.alert = comment_a.recent
        getProfile.save()

        if(how_many_filter):
            show_alert = Commentalertcontent.objects.filter(profile_name=getProfile, view=True)[:5]
            qs_json = serializers.serialize('json', show_alert, use_natural_foreign_keys=True) #use_natural_foreigin_keys를 이용해 pk가 아닌 특정 내용을 가져오도록 설정 Commentalertcontent 테이블에 def로 설정해야됨!
            qs_json = json.loads(qs_json)
        else:
            show_alert = Commentalertcontent.objects.filter(profile_name=getProfile, view=True)[:5]
            qs_json = serializers.serialize('json', show_alert, use_natural_foreign_keys=True)
            qs_json = json.loads(qs_json)

        return HttpResponse(json.dumps({'show_alert':qs_json}), 'application/json')

#알림내용삭제
@login_required(login_url='/')
def del_alert_board(request, alert_id):
    if alert_id == "all":
        del_alert = Commentalertcontent.objects.filter(profile_name=request.user.profile)
        del_alert.delete()
    else:
        del_alert = get_object_or_404(Commentalertcontent, profile_name=request.user.profile, id=alert_id)
        del_alert.delete()

    return redirect("/account/alert_board/")

