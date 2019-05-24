from django.db import models

class Crime(models.Model):
    location = models.CharField(max_length=200)
    primary_type = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
