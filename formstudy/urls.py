from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from mainpage.views import main_show

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('board/', include('usingform.urls', namespace='forms')),
    path('youtube/', include('youtube.urls', namespace='youtube')),
    path('category/', include('category.urls', namespace='category')),
    # path('', lambda r: redirect('category:show_category'), name='root'),
    path('', main_show, name='root'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
