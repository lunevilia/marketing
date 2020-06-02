from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
import json

# Create your views here.
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