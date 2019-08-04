from ..models import Crime
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
import pandas as pd
import hdbscan

class Clustering:
    def generate_data_frame(data):
        variables = data[0].keys()
        df = pd.DataFrame(data, columns = variables)
        include = ['latitude' , 'longitude']
        return df[include]

    def dbscan(data_frame, params):
        eps = 0.015
        if params['eps'] != 'None':
          eps = float(params['eps'])
        min_samples = 5
        if params['min_sample_size'] != 'None':
          min_samples = int(params['min_sample_size'])
        return DBSCAN(eps, min_samples).fit(data_frame).labels_

    def hdbscan(data_frame, params):
        min_cluster_size = 5
        if params['min_cluster_size'] != 'None':
          min_cluster_size = int(params['min_cluster_size'])
        min_samples = None
        if params['min_sample_size'] != 'None':
          min_samples = int(params['min_sample_size'])
        return hdbscan.HDBSCAN(min_cluster_size, min_samples).fit(data_frame).labels_

    def kmeans(data_frame, params):
        n_clusters = 8
        if params['n_clusters'] != 'None':
          n_clusters = int(params['n_clusters'])
        return KMeans(n_clusters).fit(data_frame).labels_

    def run_algorithm(data_frame, algorithm, algorithm_params):
        if algorithm == 'DBSCAN':
          labels = Clustering.dbscan(data_frame, algorithm_params)
        elif algorithm == 'HDBSCAN':
          labels = Clustering.hdbscan(data_frame, algorithm_params)
        else:
          labels = Clustering.kmeans(data_frame, algorithm_params)
        return labels

    def build_model(data_frame, labels):
        df_list = data_frame.values.tolist()
        models = []
        for i in range(len(data_frame)):
          model = {'latitude': df_list[i][0], 'longitude': df_list[i][1], 'label': labels[i]}
          models.append(model)
        return models

    def clusterize(data, algorithm, algorithm_params):
        df_ = Clustering.generate_data_frame(data)
        labels = Clustering.run_algorithm(df_, algorithm, algorithm_params)
        return Clustering.build_model(df_, labels)
