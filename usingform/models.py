from django.db import models
from category.models import Category
# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Defaultform(TimeStampedModel):
    title = models.CharField(max_length=200)
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,)

    class Meta:
        ordering = ['-id', ]

    def __str__(self):
        return self.title