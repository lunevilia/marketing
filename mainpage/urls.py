from django.urls import path
from . import views

app_name = "mainpage"
# url의 이름을 category로 정의하겠다
    # 이유는 다른 app들과의 차이를 알려주기 위해서 정의한다

urlpatterns = [
    path('', views.main_show, name='main'),
]
