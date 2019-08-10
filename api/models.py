from django.db import models

class Crime(models.Model):
    occured_at = models.DateTimeField(null=True)
    primary_type = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    location_description = models.CharField(max_length=200, null=True)
    arrest = models.BooleanField(default=True)
    domestic = models.BooleanField(default=True)
    distrct = models.IntegerField(null=True)
    community_areas = models.IntegerField(null=True)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    year = models.IntegerField(null=True)
    crime_weight = models.FloatField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
