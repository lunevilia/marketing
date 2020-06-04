from django.urls import path
from . import views

app_name = 'forms' 

urlpatterns = [
    path('', views.selectform, name='selectform'),
    path('<board>/', views.selectform, name='selectform'),
    path('comment/<board>/<int:id>/', views.comment_write, name='comment_write'),
    path('recomment/<board>/<int:id>/<int:comment_id>/', views.recomment_write, name='recomment_write'),
    path('modify/<board>/<int:id>/', views.mod_form, name='mod_form'),
    path('<board>/<int:id>/', views.shw_form, name='shw_form'),
    path('delete/<board>/<int:id>/', views.del_form, name='del_form'),
]
