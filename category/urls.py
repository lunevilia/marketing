from django.urls import path
from . import views

app_name = "category"

urlpatterns = [
    path('', views.show_category, name='show_category'),
    path('delete/<int:id>/', views.delete_category, name='delete_category'),
    path('modify/<int:id>/', views.mod_category, name='mod_category'),
]
