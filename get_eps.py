from api.models import Crime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

def data(number):
    data = Crime.objects.order_by('occured_at')[:number].values()
    variables = data[0].keys()
    dataframe = pd.DataFrame(data, columns=variables)
    include = ['latitude', 'longitude']
    df = dataframe[include]
    return np.array(df)

def plot(number):
    X = data(number)
    neigh = NearestNeighbors(n_neighbors=2)
    nbrs = neigh.fit(X)
    distances, indices = nbrs.kneighbors(X)
    distances = np.sort(distances, axis=0)
    distances = distances[:,1]
    plt.plot(distances)
    plt.ylabel("k-distances")
    plt.grid(True)
    plt.show()
