from django.db import models
from video_category.models import V_Category

class TimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Video(TimeModel):
    v_title = models.CharField(max_length = 30)
    v_body = models.TextField()
    v_category = models.ForeignKey(V_Category, on_delete = models.CASCADE, )