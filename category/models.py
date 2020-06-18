from django.db import models
from django.core.validators import MinValueValidator 

# Create your models here.
class Category(models.Model):
    board_name = models.CharField(max_length=50, unique=True)
    important = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        ordering = ['important', ]

    def __str__(self):
        return self.board_name
