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

    def run_algorithm(data_frame, algorithm):
        if algorithm == 'DBSCAN':
          labels = DBSCAN(eps=0.015).fit(data_frame).labels_
        elif algorithm == 'HDBSCAN':
          labels = hdbscan.HDBSCAN().fit(data_frame).labels_
        else:
          labels = KMeans().fit(data_frame).labels_
        return labels

    def build_model(data_frame, labels):
        df_list = data_frame.values.tolist()
        models = []
        for i in range(len(data_frame)):
          model = {'latitude': df_list[i][0], 'longitude': df_list[i][1], 'label': labels[i]}
          models.append(model)
        return models

    def clusterize(data, algorithm):
        df_ = Clustering.generate_data_frame(data)
        labels = Clustering.run_algorithm(df_, algorithm)
        return Clustering.build_model(df_, labels)
