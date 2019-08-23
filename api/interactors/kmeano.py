from math import floor

def run(data_frame, sample_weights, params):
    total_weight = len(data_frame)
    if params['use_weights'] == 'True':
        total_weight = sum(sample_weights)

    max_clusters = 20
    if params['min_cluster_weight'] != 'None':
        min_cluster_weight = int(params['min_cluster_weight'])
        max_clusters = floor(total_weight/min_cluster_weight)

    min_clusters = 2
    if params['max_cluster_weight'] != 'None':
        max_cluster_weight = int(params['max_cluster_weight'])
        min_clusters = floor(total_weight/max_cluster_weight)

    if sample_weights == None:
        sample_weights = ([1] * (len(data_frame)))

    k = floor((max_clusters + min_clusters)/2)
    return kmeano(k, sample_weights)

def kmeano(k, sample_weights):
    centers = KMeans(k).fit(data_frame, sample_weight=sample_weights).cluster_centers_
    center_matrix = generate_matrix(centers)
    center_mst = generate_mst(center_matrix)
    cluster_weights = calculate_cluster_weights(labels, sample_weights)
    while not satisfies_minmax(cluster_weights):
        most_unbalanced_cluster = find_unbalanced_cluster(cluster_weights)
        processed_clusters = []
        labels = rebalance(most_unbalanced_cluster, labels, cluster_weights, center_mst, processed_clusters)
        cluster_weights = calculate_cluster_weights(labels, sample_weights)
    return labels


def rebalance(cluster, labels, cluster_weights, center_mst, processed_clusters):
    # recursive
    processed_clusters += [cluster]
    neighbors = get_neighbors(cluster, center_mst, processed_clusters)
    median_weight = calculate_median_weight(cluster, neighbors)
    for neighbors in neighbors:
        balance(cluster, neighbor, median_weight)
    for neighbors in neighbors:
        rebalance(neighbor, labels, cluster_weights, center_mst, processed_clusters)

def balance(cluster, neighbor, median_weight):
    n = npoints_to_transfer(cluster, neighbor, median_weight)
    border_points = find_border_points(cluster, neighbor, n)
    transfer_points(border_points, labels, cluster, neighbor)

def npoints_to_transfer(cluster, neighbor, median_weight):
    # returns amount of points to be transferred so that:
    # 1) both clusters end up with same weight
    # 2) clusters end up with a weight equal to median_weight if posible
    1

def get_neighbors(cluster, center_mst, processed_clusters):
    # return not processed neighbors
    1

def calculate_median_weight(cluster, neighbors):
    # return median weight between cluster and neighbors
    1

def find_border_points(biggest_cluster, neighbor, n):
    # return n border points in biggest_cluster with respect to neighbor
    1

def transfer_points(points, labels, origin, destiny):
    # transfer points from origin cluster to destiny cluster
    1

def generate_matrix(centers):
    # return distance matrix for cluster centers
    1

def generate_mst(center_matrix):
    # return minimum spanning tree from center_matrix
    1

def find_unbalanced_cluster(cluster_weights):
    # returns most unbalanced cluster (biggest or smallest) with respect to ideal average weight
    1

def satisfies_minmax(k, labels, sample_weights, min_cluster_weight, max_cluster_weight):
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
