from django.db import models
from category.models import Category
from account.models import Profile
from django.contrib.auth.models import User
from django import template
from django.core.validators import MinValueValidator 

from django.conf import settings
from PIL import Image as Img
from PIL import ExifTags
from io import BytesIO
from django.core.files import File

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

    def mylike(self):
        return Like.objects.filter(post=self).count()

    def title_short(self):
        if len(self.title)>20:
            return self.title[:20]+"..."
        else:
            return self.title

    # def comment_count(self):
    #     self.comment_set

class Image(TimeStampedModel):
    post = models.ForeignKey(Defaultform, on_delete=models.CASCADE,)
    image = models.ImageField(upload_to='board_picture/', null=True, blank=True)

    def __str__(self):
        return str(self.image)

    def save(self, *args, **kwargs): #저장할때 이미지는 orientation 맞춰서 저장 또한 전부 삭제 exif정보
        if self.image:
            pilImage = Img.open(BytesIO(self.image.read()))
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(pilImage._getexif().items())

                if exif[orientation] == 3:
                    pilImage = pilImage.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    pilImage = pilImage.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    pilImage = pilImage.rotate(90, expand=True)

                output = BytesIO()
                pilImage.save(output, format='JPEG', quality=75)
                output.seek(0)
                self.image = File(output, self.image.name)
            except:
                pass

        return super(Image, self).save(*args, **kwargs)

class Files(TimeStampedModel):
    post = models.ForeignKey(Defaultform, on_delete=models.CASCADE,)
    files = models.FileField(upload_to='board_file/', null=True, blank=True)

    def __str__(self):
        return str(self.files)

class Like(TimeStampedModel):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    post = models.ForeignKey(Defaultform, on_delete=models.CASCADE,)

    class Meta:
        ordering = ['-id', ]

    def __str__(self):
        return str(self.post)

class Favorite(TimeStampedModel):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    post = models.ForeignKey(Defaultform, on_delete=models.CASCADE,)

    def __str__(self):
        return str(self.post)

class Comment(TimeStampedModel):
    main_post = models.ForeignKey(Defaultform, on_delete=models.CASCADE)
    post = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    body = models.TextField()

    def __str__(self):
        return '%s - %s - %s' % (self.main_post, self.post, self.body)

    def mylike(self):
        return CommentLike.objects.filter(post=self).count()

    def natural_key(self): #json serialize 에서 특정 내용만 가져오기 위해서 설정 원래는 pk 정보만 나오는데 이렇게 설정
        return (self.body)

class CommentLike(TimeStampedModel):
    post = models.ForeignKey(Comment, on_delete=models.CASCADE,)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,)

    def __str__(self):
        return '%s - %s' % (self.post, self.author)

#알람 내용
class Commentalertcontent(TimeStampedModel):
    profile_name = models.ForeignKey(Profile, on_delete=models.CASCADE) # models.CharField(max_length=300)
    sender_name = models.CharField(max_length=300)
    board = models.ForeignKey(Defaultform, on_delete=models.CASCADE)
    content = models.ForeignKey(Comment, on_delete=models.CASCADE)
    view = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id', ]

    def __str__(self):
        return '%s - %s - %s' % (self.profile_name.Name, self.board, self.content)

    def natural_key(self): #json serialize 에서 특정 내용만 가져오기 위해서 설정 원래는 pk 정보만 나오는데 이렇게 설정
        return (self.content)


#알람 차단하기
class Donotalert(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    board = models.ForeignKey(Defaultform, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id', ]

    def __str__(self):
        return '%s - %s' % (self.profile, self.board)

#공지 게시판
class Important_board(models.Model):
    post = models.ForeignKey(Defaultform, on_delete=models.CASCADE)
    important = models.FloatField(default=0,validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['-important', ]

    def __str__(self):
        return '%s - %s' % (self.post, self.important)