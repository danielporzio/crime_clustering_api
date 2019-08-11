import pandas as pd
import hdbscan
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans

def clusterize(data, algorithm, algorithm_params):
    df_ = generate_data_frame(data)
    sample_weights = get_weights(data, algorithm_params['use_weights'])
    labels = run_algorithm(df_, sample_weights, algorithm, algorithm_params)
    return build_model(df_, labels)

def generate_data_frame(data):
    variables = data[0].keys()
    dataframe = pd.DataFrame(data, columns=variables)
    include = ['latitude', 'longitude']
    return dataframe[include]

def get_weights(data, use_weights):
    sample_weights = None
    if use_weights == 'True':
        sample_weights = [x["crime_weight"] for x in data]
    return sample_weights

def run_algorithm(data_frame, sample_weights, algorithm, algorithm_params):
    if algorithm == 'DBSCAN':
        labels = dbscan(data_frame, sample_weights, algorithm_params)
    elif algorithm == 'HDBSCAN':
        labels = hdbscan_algorithm(data_frame, algorithm_params)
    else:
        labels = kmeans(data_frame, sample_weights, algorithm_params)
    return labels

def build_model(data_frame, labels):
    df_list = data_frame.values.tolist()
    models = []
    for i in range(len(data_frame)):
        model = {'latitude': df_list[i][0], 'longitude': df_list[i][1], 'label': labels[i]}
        models.append(model)
    return models

def dbscan(data_frame, sample_weights, params):
    eps = 0.015
    if params['eps'] != 'None':
        eps = float(params['eps'])
    min_samples = 5
    if params['min_sample_size'] != 'None':
        min_samples = int(params['min_sample_size'])
    return DBSCAN(eps, min_samples).fit(data_frame, sample_weights).labels_

def hdbscan_algorithm(data_frame, params):
    min_cluster_size = 5
    if params['min_cluster_size'] != 'None':
        min_cluster_size = int(params['min_cluster_size'])
    min_samples = None
    if params['min_sample_size'] != 'None':
        min_samples = int(params['min_sample_size'])
    return hdbscan.HDBSCAN(min_cluster_size, min_samples).fit(data_frame).labels_

def kmeans(data_frame, sample_weights, params):
    n_clusters = 8
    if params['n_clusters'] != 'None':
        n_clusters = int(params['n_clusters'])
    return KMeans(n_clusters).fit(data_frame, sample_weights).labels_
