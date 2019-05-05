from django.db import models

# Create your models here.
class Crime(models.Model):
    location = models.CharField(max_length=200)
    primary_type = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
