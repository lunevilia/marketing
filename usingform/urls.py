from django.urls import path
from . import views

app_name = 'forms' 

urlpatterns = [
    path('', views.selectform, name='selectform'),
    path('<board>/', views.selectform, name='selectform'),

    #댓글 생성
    path('comment/<board>/<int:id>/', views.comment_write, name='comment_write'),
    path('recomment/<board>/<int:id>/<int:comment_id>/', views.recomment_write, name='recomment_write'),
    #댓글 삭제
    path('comment_del/<board>/<int:id>/<int:comment_id>/', views.comment_del, name='comment_del'),

    #좋아요
    path('ajax_comment_like/<int:comment_id>/', views.ajax_comment_like, name='ajax_comment_like'),
    path('ajax_board_like/<int:id>/', views.ajax_board_like, name='ajax_board_like'),

    #즐겨찾기
    path('ajax_board_favorite/<int:id>/', views.ajax_board_favorite, name='ajax_board_favorite'),

    #알람차단 및 설정
    path('ajax_donot_alert/<int:id>/', views.ajax_donot_alert, name='ajax_donot_alert'),

    #조회, 수정, 삭제
    path('modify/<board>/<int:id>/', views.mod_form, name='mod_form'),
    path('<board>/<int:id>/', views.shw_form, name='shw_form'),
    path('delete/<board>/<int:id>/', views.del_form, name='del_form'),
]