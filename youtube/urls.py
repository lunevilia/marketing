from django.urls import path
from . import views

app_name = "youtube"

urlpatterns = [
    path('', views.channel, name='channel'),
    path('playlist/', views.playlist, name='playlist'),
    path('<gettype>/<token>/', views.ajax, name='ajax')
]
