from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from PIL import Image as Img
from PIL import ExifTags
from io import BytesIO
from django.core.files import File

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=16, unique=True)
    Image = models.ImageField(upload_to='profile/', null=True, blank=True)
    Email = models.EmailField(null=True, blank=False, unique=True)
    alert = models.IntegerField(default=0)

    def __str__(self):
        return self.Name
    
    def save(self, *args, **kwargs): #저장할때 이미지는 orientation 맞춰서 저장 또한 전부 삭제 exif정보
        if self.Image:
            pilImage = Img.open(BytesIO(self.Image.read()))
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
                self.Image = File(output, self.Image.name)
            except:
                pass

        return super(Profile, self).save(*args, **kwargs)

class Commentalert(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    recent = models.IntegerField(default=0)

    def __str__(self):
        return '%s - %s' % (self.profile.Name, self.recent)