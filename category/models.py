from django.db import models
from django.core.validators import MinValueValidator 
from colorfield.fields import ColorField

# Create your models here.
class Category(models.Model):
    board_name = models.CharField(max_length=50, unique=True)
    # “게시글 테이블” 이 Category 테이블을 참조하여 게시글 종류(board_name)별로 나눌 수 있도록 하기 위해서 사용
        # unique를 이용하여 똑같은 이름을 가진 게시글은 생성하지 못하도록 설정
    important = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    # important를 이용하여 만들어진 게시판 종류의 순서를 바꾸기 위해서 정의
        # PositiveIntegerField로 한 이유는 1~ 양수만 나타낼 수 있도록 하기 위해서 사용
        # validators는 PositiveIntegerField는 0의 값도 받아서 1이 최소값으로 하기 위해 정의
    color = ColorField(blank=True)
    # 만들어 질 때 같이 이용해서 수정 할 때도 게시판 색깔을 바꿀 수 있도록 생성

    class Meta:
        ordering = ['important', ]
        #정렬은 important 오름차 순으로 정렬

    def __str__(self):
        return self.board_name
