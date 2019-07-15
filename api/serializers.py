from rest_framework import serializers
from .models import Crime

class CrimeSerializer(serializers.ModelSerializer):
    label=serializers.SerializerMethodField()
    def get_label(self, obj):
        return obj['label']
    class Meta:
        model = Crime
        fields=('latitude','longitude','label')
