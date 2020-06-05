from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=16, unique=True)
    Image = models.ImageField(upload_to='profile/', null=True, blank=True)
    Email = models.EmailField(null=True, blank=False, unique=True)
    alert = models.IntegerField(default=0)

    def __str__(self):
        return self.Name

class Commentalert(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    recent = models.IntegerField(default=0)

    def __str__(self):
        return '%s - %s' % (self.profile.Name, self.recent)