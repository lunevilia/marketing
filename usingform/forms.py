from django import forms
from .models import *

class FormTest(forms.ModelForm):
    class Meta:
        model = Defaultform
        fields = ('title', 'body')
        labels = { 'title': '제목', 'body':'내용'}
        #help_texts = { 'title': '필수 사항 입니다!', 'body':'내용을 입력해주세요!'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'title'}),
        }