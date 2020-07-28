from django.contrib import admin
from .models import Tag, Defaultform, Image, Files, Like, Favorite, Comment, CommentLike, Commentalertcontent, Donotalert, Important_board

admin.site.register(Defaultform)
admin.site.register(Image)
admin.site.register(Files)
admin.site.register(Like)
admin.site.register(Favorite)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Commentalertcontent)
admin.site.register(Donotalert)
admin.site.register(Important_board)
admin.site.register(Tag)

