from rest_framework import generics
from .serializers import CrimeSerializer
from .models import Crime


class CreateView(generics.ListCreateAPIView):
  serializer_class = CrimeSerializer
  def perform_create(self, serializer):
    serializer.save()

  def get_queryset(self):
    model = Crime.objects
    for k,vals in self.request.GET.lists():
      for v in vals:
        model = model.filter(**{k: v})
    return model

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Crime.objects.all()
    serializer_class = CrimeSerializer
