from django.db import models
from category.models import Category
from account.models import Profile
from django.contrib.auth.models import User
from django import template

register = template.Library()

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Defaultform(TimeStampedModel):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,)

    class Meta:
        ordering = ['-id', ]

    def __str__(self):
        return self.title

class Image(TimeStampedModel):
    post = models.ForeignKey(Defaultform, on_delete=models.CASCADE,)
    image = models.ImageField(upload_to='board_picture/', null=True, blank=True)

    def __str__(self):
        return self.image

class Files(TimeStampedModel):
    post = models.ForeignKey(Defaultform, on_delete=models.CASCADE,)
    files = models.FileField(upload_to='board_file/', null=True, blank=True)

    def __str__(self):
        return self.files

class Like(TimeStampedModel):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    post = models.ForeignKey(Defaultform, on_delete=models.CASCADE,)

    def __str__(self):
        return self.post

class Favorite(TimeStampedModel):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    post = models.ForeignKey(Defaultform, on_delete=models.CASCADE,)

    def __str__(self):
        return self.post

class Comment(TimeStampedModel):
    main_post = models.ForeignKey(Defaultform, on_delete=models.CASCADE)
    post = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    body = models.TextField()

    def __str__(self):
        return '%s - %s - %s' % (self.main_post, self.post, self.body)

    def mylike(self):
        return CommentLike.objects.filter(post=self).count()

class CommentLike(TimeStampedModel):
    post = models.ForeignKey(Comment, on_delete=models.CASCADE,)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,)

    def __str__(self):
        return '%s - %s' % (self.post, self.author)