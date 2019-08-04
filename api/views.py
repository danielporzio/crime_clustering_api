from rest_framework import generics
from .serializers import CrimeSerializer
from .models import Crime
from .interactors.clustering import Clustering

class CreateView(generics.ListCreateAPIView):
  serializer_class = CrimeSerializer
  def perform_create(self, serializer):
    serializer.save()

  def get_queryset(self):
    model = Crime.objects
    params = self.request.GET.copy()

    algorithm = params.pop('algorithm', ['None'])[0]
    algorithm_params = {}
    algorithm_params['eps'] = params.pop('epsilon', ['None'])[0]
    algorithm_params['min_cluster_size'] = params.pop('minClusterSize', ['None'])[0]
    algorithm_params['min_sample_size'] = params.pop('minSamples', ['None'])[0]
    algorithm_params['n_clusters'] = params.pop('numberClusters', ['None'])[0]

    filteredAtt = []
    for k,vals in params.lists():
      tmp_model = None
      for v in vals:
        if not tmp_model:
          tmp_model = model.filter(**{k: v})
        aux = model.filter(**{k: v})
        newmodel = tmp_model.union(aux)
      filteredAtt.append(newmodel)

    if len(filteredAtt) > 0:
      model = filteredAtt[0]
      for f in filteredAtt:
        model = model.intersection(f)

    if algorithm == 'None':
        return model
    else:
        return Clustering.clusterize(model.values(), algorithm, algorithm_params)

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Crime.objects.all()
  serializer_class = CrimeSerializer
