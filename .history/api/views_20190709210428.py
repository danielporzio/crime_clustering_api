from rest_framework import generics
from .serializers import CrimeSerializer
from .models import Crime


class CreateView(generics.ListCreateAPIView):
  """This class defines the create behavior of our rest api."""
  """queryset = Crime.objects.all()"""
  serializer_class = CrimeSerializer
  def perform_create(self, serializer):
    """Save the post data when creating a new bucketlist."""
    serializer.save()

  def get_queryset(self):
    print("ggg")
    """
    This view should return a list of all the purchases
    for the currently authenticated user.
    """
    return Crime.objects.filter(primary_type="THEFT")

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Crime.objects.all()
    serializer_class = CrimeSerializer
