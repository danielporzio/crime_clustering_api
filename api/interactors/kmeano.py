from math import floor
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import KMeans
from scipy.sparse.csgraph import shortest_path

class Kmeano:
    def __init__(self, data_frame, sample_weights):
        self.data_frame      = data_frame
        self.sample_weights  = sample_weights
        self.labels          = None
        self.center_mst      = None
        self.cluster_weights = None

    def run(self, params):
        k = self.find_number_of_clusters(params)
        kmeans = KMeans(k).fit(self.data_frame, sample_weight=self.sample_weights)
        centers = kmeans.cluster_centers_
        self.labels = kmeans.labels_
        self.center_mst = self.generate_mst(centers)
        self.cluster_weights = self.calculate_cluster_weights()
        while not self.satisfies_minmax(cluster_weights):
            processed_clusters      = []
            most_unbalanced_cluster = self.find_unbalanced_cluster()
            self.labels             = self.rebalance(most_unbalanced_cluster, processed_clusters)
            self.cluster_weights    = self.calculate_cluster_weights()
        return labels

    def find_number_of_clusters(self, params):
        total_weight = len(self.data_frame)
        if params['use_weights'] == 'True':
            total_weight = sum(self.sample_weights)

        max_clusters = 20
        if params['min_cluster_weight'] != 'None':
            min_cluster_weight = int(params['min_cluster_weight'])
            max_clusters = floor(total_weight / min_cluster_weight)

        min_clusters = 2
        if params['max_cluster_weight'] != 'None':
            max_cluster_weight = int(params['max_cluster_weight'])
            min_clusters = floor(total_weight / max_cluster_weight)
        return floor((max_clusters + min_clusters) / 2)

    def rebalance(self, cluster, processed_clusters):
        # recursive
        processed_clusters += [cluster]
        neighbors = self.get_neighbors(cluster, processed_clusters)
        median_weight = self.calculate_median_weight(cluster, neighbors)
        for neighbors in neighbors:
            self.balance(cluster, neighbor, median_weight)
        for neighbors in neighbors:
            self.rebalance(most_unbalanced_cluster, processed_clusters)

    def balance(self, cluster, neighbor, median_weight):
        n = self.weight_to_transfer(cluster, neighbor, median_weight)
        border_points = self.find_border_points(cluster, neighbor, n)
        self.transfer_points(border_points, labels, cluster, neighbor)

    def weight_to_transfer(self, cluster, neighbor, median_weight):
        # returns amount of points to be transferred so that:
        # 1) both clusters end up with same weight
        # 2) clusters end up with a weight equal to median_weight if posible
        return True

    def get_neighbors(self, cluster, processed_clusters):
        # return not processed neighbors
        return True

    def calculate_median_weight(self, cluster, neighbors):
        # return median weight between cluster and neighbors
        return True

    def find_border_points(self, biggest_cluster, neighbor, n):
        # return n border points in biggest_cluster with respect to neighbor
        return True

    def calculate_cluster_weights(self):
        return True

    def transfer_points(self, points, origin, destiny):
        # transfer points from origin cluster to destiny cluster
        return True

    def generate_mst(self, centers):
        # return minimum spanning tree from center_matrix
        clusters_distances = pairwise_distances(centers)
        return shortest_path(clusters_distances, 'auto')

    def find_unbalanced_cluster(self):
        # returns most unbalanced cluster (biggest or smallest) with respect to ideal average weight
        return True

    def satisfies_minmax(self, k, min_cluster_weight, max_cluster_weight):
        label_list = self.labels.tolist()
        weights_list = self.sample_weights
        if self.sample_weights is None:
            weights_list = ([1] * len(self.labels))
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
