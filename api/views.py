from rest_framework import generics
from .serializers import CrimeSerializer
from .models import Crime
from .interactors import clustering

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
        algorithm_params['use_weights'] = params.pop('useWeights', ['None'])[0]

        filtered_attributes = []
        for k, vals in params.lists():
            tmp_model = None
            for value in vals:
                if not tmp_model:
                    tmp_model = model.filter(**{k: value})
                    aux = model.filter(**{k: value})
                    newmodel = tmp_model.union(aux)
                    filtered_attributes.append(newmodel)

        if filtered_attributes:
            model = filtered_attributes[0]
            for attribute in filtered_attributes:
                model = model.intersection(attribute)
        model = model.all()[:10000]
        if algorithm == 'None':
            return model
        return clustering.clusterize(model.values(), algorithm, algorithm_params)

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Crime.objects.all()
    serializer_class = CrimeSerializer
