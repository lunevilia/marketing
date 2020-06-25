from django.urls import path
from . import views

app_name = "category"
# url의 이름을 category로 정의하겠다
    # 이유는 다른 app들과의 차이를 알려주기 위해서 정의한다

urlpatterns = [
    # show_category : 게시판의 종류를 보여주고 작성하기 (GET : 보여주기, POST : 작성하기)
    path('', views.show_category, name='show_category'),

    # delete_category : 게시판의 종류를 삭제하기 (GET : 삭제하기, POST : 삭제하기)
    path('delete/<int:id>/', views.delete_category, name='delete_category'),

    # mode_category : 작성한 게시판 종류의 정보를 수정하기 (POST : 수정하기)
    path('modify/<int:id>/', views.mod_category, name='mod_category'),
]
