from django.conf.urls import url, include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import CreateView, DetailsView

urlpatterns = {
  path('crimes/', CreateView.as_view(), name='create'),
  path('crimes/<int:pk>/', DetailsView.as_view(), name='details'),
  path('clustering/', views.clustering, name='clustering')
}

urlpatterns = format_suffix_patterns(urlpatterns)
