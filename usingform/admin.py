from django.contrib import admin
from .models import Defaultform, Image, Files, Like, Favorite

admin.site.register(Defaultform)
admin.site.register(Image)
admin.site.register(Files)
admin.site.register(Like)
admin.site.register(Favorite)