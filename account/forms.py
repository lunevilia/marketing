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