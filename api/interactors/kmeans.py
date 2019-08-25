import pandas as pd
from sklearn.cluster import KMeans
from math import floor, ceil
from numpy.random import randint

def run(data_frame, sample_weights, params):
    n_clusters = 8
    if params['n_clusters'] != 'None':
        n_clusters = int(params['n_clusters'])

    if params['min_max'] == 'True':
        return minmax(data_frame, sample_weights, params)
    else:
        return KMeans(n_clusters).fit(data_frame, sample_weight=sample_weights).labels_

def minmax(data_frame, sample_weights, params):
    total_weight = len(data_frame)
    if params['use_weights'] == 'True':
        total_weight = sum(sample_weights)

    max_clusters = 50
    if params['min_cluster_weight'] != 'None':
        min_cluster_weight = int(params['min_cluster_weight'])
        max_clusters = floor(total_weight/min_cluster_weight)

    min_clusters = 2
    if params['max_cluster_weight'] != 'None':
        max_cluster_weight = int(params['max_cluster_weight'])
        min_clusters = floor(total_weight/max_cluster_weight)

    if sample_weights == None:
        sample_weights = ([1] * (len(data_frame)))

    return find_number_of_clusters(data_frame, sample_weights, min_clusters, max_clusters, min_cluster_weight, max_cluster_weight)

def find_number_of_clusters(data_frame, sample_weights, min_clusters, max_clusters, min_cluster_weight, max_cluster_weight):
    # increment = ceil((max_clusters - min_clusters) / 10)
    if ((max_clusters - min_clusters) > 20):
        increment = 2
    else:
        increment = 1

    k = min_clusters
    satisfies = False
    while (k <= max_clusters) and (not satisfies):
        clustering = KMeans(k).fit(data_frame, sample_weight=sample_weights)
        satisfies = satisfies_minmax(k, clustering.labels_, sample_weights, min_cluster_weight, max_cluster_weight)
        k += increment
    if satisfies:
        return clustering.labels_
    else:
        return ([-1] * (len(clustering.labels_)))

def satisfies_minmax(k, labels , sample_weights, min_cluster_weight, max_cluster_weight):
    label_list = labels.tolist()
    weights_list = sample_weights
    if sample_weights == None:
        weights_list = ([1] * (len(labels)))
    label_weights = zip(label_list, weights_list)
    weights_array = ([0] * k)
    for x, y in label_weights:
        weights_array[x] += y
    for size in weights_array:
        if size < min_cluster_weight:
            return False
        if size > max_cluster_weight:
            return False
    return True
