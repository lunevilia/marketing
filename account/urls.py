from django.urls import path
from . import views
#from django.contrib.auth import views as auth_views

app_name = 'account' 

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('ajax/<value>/<region>/', views.ajax, name='ajax'),
]
