from rest_framework import serializers
from .models import Crime

class CrimeSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Crime
        fields = '__all__'
