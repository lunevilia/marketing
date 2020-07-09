from django import forms
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        # Category 테이블 기준으로 form을 정의하겠다
        fields = '__all__'
        # Category 테이블의 모든 필드를 입력하도록 하겠다
        error_messages = {
            'board_name': {
                'unique': "동일한 게시판이 존재 합니다!! 다른 게시판을 입력해주세요!",
            },
        }
        # 애러 메세지 중에서 'board_name'(게시판이름)의 unique에 관한 애러가 발생하면 에러 메세지로 "동일한 게시판이 .... "으로 출력하도록 하겠다
        labels = { 
            'board_name': '게시판 추가',
            'important' : '게시판 순서',
            'color' : '게시판 색깔'
        }
        # form을 html에 띄울때, 해당 label들의 표시를 'board_name'과 같이 필드명으로 하지 않고, '게시판 추가' 처럼 사용자가 직접 정의하겠다
 