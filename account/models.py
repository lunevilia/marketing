from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=16, unique=True)
    Image = models.ImageField(upload_to='profile/', null=True, blank=True)
    Email = models.EmailField(null=True, blank=False, unique=True)

    def __str__(self):
        return self.Name