from django import forms
from .models import *

class SignupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('Name', 'Image', 'Email',)
        labels = {
            'Name': '닉네임',
            'Image': '프로필 사진',
            'Email': '이메일',
        }
        widgets = {
            'Name': forms.TextInput(attrs={'id': 'nickname_id', 'onchange':"rematch(this.id)", }),
            'Email': forms.TextInput(attrs={'id': 'email_id', 'onchange':"rematch(this.id)",}),
        }

        onchange="rematch(this.id)"

class ModifyForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('Name', 'Image', )
        labels = {
            'Name': '닉네임',
            'Image': '프로필 사진',
        }
        widgets = {
            'Name': forms.TextInput(attrs={'id': 'nickname_id', 'onchange':"rematch(this.id)", }),
        }
        error_messages = {
            'Name': {
                'unique': "동일한 닉네임이 존재합니다!",
            },
        }

        onchange="rematch(this.id)"