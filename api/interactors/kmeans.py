from sklearn.cluster import KMeans

def run(data_frame, sample_weights, params):
    n_clusters = 8
    if params['n_clusters'] != 'None':
        n_clusters = int(params['n_clusters'])
        return KMeans(n_clusters).fit(data_frame, sample_weight=sample_weights).labels_
