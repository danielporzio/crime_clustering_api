from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from .serializers import CrimeSerializer
from .models import Crime
from .clustering import hdbscan


class CreateView(generics.ListCreateAPIView):
  serializer_class = CrimeSerializer
  def perform_create(self, serializer):
    serializer.save()

  def get_queryset(self):
    model = Crime.objects
    params = self.request.GET.copy()
    algorithm = params.pop('algorithm', 'None')[0]
    for k,vals in params.lists():
      for v in vals:
        model = model.filter(**{k: v})
    if algorithm == 'None':
        return model
    else:
        return model

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Crime.objects.all()
  serializer_class = CrimeSerializer
