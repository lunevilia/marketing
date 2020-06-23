from django import forms
from .models import *
from django.forms.widgets import ClearableFileInput

class MyClearableFileInput(ClearableFileInput):
    initial_text = '현재 사진'
    input_text = '사진 바꾸기'
    clear_checkbox_label = '지우기'
        
class SignupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('Name', 'Image', 'Email',)
        labels = {
            'Name': '',
            'Image': '',
            'Email': '',
        }
        widgets = {
            'Name': forms.TextInput(attrs={
                'id': 'nickname_id',
                'onchange':'rematch(this.id)',
                'placeholder':'🎭닉네임',
                'style':'text-align:center',
                'required':True,
                }),
            'Email': forms.EmailInput(attrs={'id': 'email_id', 'onchange':"rematch(this.id)", 'placeholder':'✉이메일','style':'text-align:center','required':True,}),
            'Image': forms.FileInput(attrs={'style':'display:none',})
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
            'Image': MyClearableFileInput,
        }
        error_messages = {
            'Name': {
                'unique': "동일한 닉네임이 존재합니다!",
            },
        }

        onchange="rematch(this.id)"