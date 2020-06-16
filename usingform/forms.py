from django import forms
from .models import *

class FormTest(forms.ModelForm):
    class Meta:
        model = Defaultform
        fields = ('title', 'body')
        labels = { 'title': '제목', 'body':'내용',}
        #help_texts = { 'title': '필수 사항 입니다!', 'body':'내용을 입력해주세요!'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ImageTest(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', )
        labels = { 'image': '이미지',}
        #help_texts = { 'title': '필수 사항 입니다!', 'body':'내용을 입력해주세요!'}
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'multiple': True,
            }),
            
        }

class FilesTest(forms.ModelForm):
    class Meta:
        model = Files
        fields = ('files', )
        labels = { 'files': '첨부파일',}
        widgets = {
            'files': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class CommentTest(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        labels = { 'body': '댓글',}
        widgets = {
            'body': forms.TextInput(attrs={'class': 'form-control', 'rows':3, 'id':False,}),
        }