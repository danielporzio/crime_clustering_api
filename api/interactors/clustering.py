# import hdbscan
from sklearn.cluster import DBSCAN
import pandas as pd
from ..models import Crime
import hdbscan
import pdb

class Clustering:
    def dbscan(data):
        clustering = DBSCAN(eps=0.015).fit(data)
        return clustering.labels_

    def hdbscan(data):
        clustering = hdbscan.HDBSCAN().fit(data)
        return clustering.labels_

    def clusterize(data, algorithm):
        variables = data[0].keys()
        df = pd.DataFrame(data, columns = variables)
        include = ['latitude' , 'longitude']
        df_ = df[include]

        if algorithm == 'DBSCAN':
          labels = Clustering.dbscan(df_)
        elif algorithm == 'DBSCAN++':
          return data
        elif algorithm == 'HDBSCAN':
          labels = Clustering.hdbscan(df_)
        else:
          return data

        df_list = df_.values.tolist()
        models = []
        for i in range(len(df_)):
          model = {'latitude': df_list[i][0], 'longitude': df_list[i][1], 'label': labels[i]}
          models.append(model)
        return models
