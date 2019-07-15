# import hdbscan
from sklearn.cluster import DBSCAN
import pandas as pd
from ..models import Crime
import pdb

class Clustering():
    def clusterize(data, algorithm):
        variables = data[0].keys()
        df = pd.DataFrame(data, columns = variables)
        include = ['latitude' , 'longitude']
        df_ = df[include]

        if algorithm == 'DBSCAN':
          clustering = DBSCAN(eps=0.015).fit(df_)
          df_list = df_.values.tolist()
          models = []
          for i in range(len(df_)):
            model = {'latitude': df_list[i][0], 'longitude': df_list[i][1], 'label': clustering.labels_[i]}
            models.append(model)
          return models
        elif algorithm == 'DBSCAN++':
          return data
        elif algorithm == 'HDBSCAN':
          return data
        else:
          return data
