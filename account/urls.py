from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account' 

urlpatterns = [
    #회원가입
    path('signup/', views.signup, name='signup'),

    #로그인
    path('login/', views.login, name='login'),

    #로그아웃
    path('logout/', auth_views.LogoutView.as_view(), kwargs={'next_page': '/'}, name='logout'),

    #회원정보 수정 requried login 추가
    path('profile/', views.profile, name='profile'),

    #회원페이지 => 내가쓴글, 쪽지보기, 즐겨찾기, 좋아요 requried login 추가
    path('like_board/', views.like_board, name='like_board'),

    #회원탈퇴
    #비밀번호 수정
    path('ajax/<value>/<region>/', views.ajax, name='ajax'),

    #알람 글 보이기
    path('notice_ajax/', views.notice_ajax, name='notice_ajax'),
]
