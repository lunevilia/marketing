from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
import json
from usingform.models import Commentalertcontent
from django.core import serializers
from django.contrib.auth.decorators import login_required

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
            error = "비밀번호를 다시 확인해주세요!"
    else:
        error = ""
        form = SignupForm()
    return render(request, "signup.html", {"form":form, "error":error,})

@login_required(login_url='/')
def profile(request):
    profile_information = Profile.objects.get(user__username=request.user)
    if request.method == "POST":
        profile_form = ModifyForm(request.POST, request.FILES, instance=profile_information)
        if profile_form.is_valid():
            profile_form.save()
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
            qs_json = serializers.serialize('json', show_alert, use_natural_foreign_keys=True) #use_natural_foreigin_keys를 이용해 pk가 아닌 특정 내용을 가져오도록 설정
            qs_json = json.loads(qs_json)
        else:
            show_alert = Commentalertcontent.objects.filter(profile_name=getProfile, view=True)[:5]
            qs_json = serializers.serialize('json', show_alert, use_natural_foreign_keys=True)
            qs_json = json.loads(qs_json)

        return HttpResponse(json.dumps({'show_alert':qs_json}), 'application/json')
