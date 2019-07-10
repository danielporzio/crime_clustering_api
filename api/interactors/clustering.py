# import hdbscan
from sklearn.cluster import DBSCAN
import pandas as pd
import pdb
from ..models import Crime

class Clustering():
    def dbscan():
        crimes = Crime.objects.all().values()
        variables = crimes[0].keys()
        df = pd.DataFrame(crimes, columns = variables)
        include = ['latitude' , 'longitude']
        df_ = df[include]
        clustering = DBSCAN(eps=0.015).fit(df_)
        return clustering.labels_


==================================
en views

        labels = Clustering.dbscan()
        from .interactors.clustering import Clustering
