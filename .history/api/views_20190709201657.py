from rest_framework import generics
from .serializers import CrimeSerializer
from .models import Crime


class CreateView(generics.ListCreateAPIView):
  """This class defines the create behavior of our rest api."""
  queryset = Crime.objects.all()
  serializer_class = CrimeSerializer
  def perform_create(self, serializer):
    """Save the post data when creating a new bucketlist."""
    serializer.save()

  def get_queryset(self):
    print(self)
    """
    This view should return a list of all the purchases
    for the currently authenticated user.
    """
    user = self.request.user
    return Crime.objects.filter(purchaser=user)

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Crime.objects.all()
    serializer_class = CrimeSerializer
