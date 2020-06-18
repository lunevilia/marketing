from django import forms
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        error_messages = {
            'board_name': {
                'unique': "동일한 게시판이 존재 합니다!! 다른 게시판을 입력해주세요!",
            },
        }
        labels = { 
            'board_name': '게시판 추가',
            'important' : '게시판 순서',
            'color' : '게시판 색깔'
        }