from django.db import models

# Create your models here.
class Category(models.Model):
    board_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.board_name
