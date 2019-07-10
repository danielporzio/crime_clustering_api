from rest_framework import generics
from .serializers import CrimeSerializer
from .models import Crime
import logging

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'django.request': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})

logger = logging.getLogger(_)

class CreateView(generics.ListCreateAPIView):
  """This class defines the create behavior of our rest api."""
  """queryset = Crime.objects.all()"""
  serializer_class = CrimeSerializer
  def perform_create(self, serializer):
    """Save the post data when creating a new bucketlist."""
    serializer.save()

  def get_queryset(self):
    logger.error("ggg")
    """
    This view should return a list of all the purchases
    for the currently authenticated user.
    """
    return Crime.objects.filter(primary_type="THEFT")

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Crime.objects.all()
    serializer_class = CrimeSerializer
