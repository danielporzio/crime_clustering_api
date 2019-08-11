from rest_framework import serializers
from .models import Crime

class CrimeSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    def get_label(self, obj):
        label = 0
        if isinstance(obj, dict):
            label = obj['label']
        return label
    class Meta:
        model = Crime
        fields=('latitude','longitude','label', 'crime_weight')
