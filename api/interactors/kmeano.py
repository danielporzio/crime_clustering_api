from math import floor
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import KMeans
from scipy.sparse.csgraph import shortest_path
import numpy as np
from scipy.spatial.distance import cdist

class Kmeano:
    # Kmeano is a Kmeans variation that allows the user to input a max and min
    # weight values for the clusters to be formed
    # It works by post-processing data obtained from the Kmeans algorithm,
    # re-assigning cluster points until the condition is met

    def __init__(self, data_frame, sample_weights):
        self.data_frame         = data_frame
        self.sample_weights     = sample_weights
        self.labels             = None
        self.centers            = None
        self.centers_mst        = None
        self.cluster_weights    = None
        self.min_cluster_weight = None
        self.max_cluster_weight = None


    def run(self, params):
        k             = self.find_number_of_clusters(params)
        kmeans_output = KMeans(k).fit(self.data_frame, sample_weight=self.sample_weights)
        self.centers  = kmeans_output.cluster_centers_
        self.labels   = kmeans_output.labels_
        self.generate_mst()
        self.calculate_cluster_weights()
        while not self.satisfies_minmax():
            processed_clusters      = []
            most_unbalanced_cluster = self.find_unbalanced_cluster()
            self.labels             = self.rebalance(most_unbalanced_cluster, processed_clusters)
            self.calculate_cluster_weights()
        return labels

    def find_number_of_clusters(self, params):
        total_weight = len(self.data_frame)
        if params['use_weights'] == 'True':
            total_weight = sum(self.sample_weights)

        max_clusters = 20
        if params['min_cluster_weight'] != 'None':
            self.min_cluster_weight = int(params['min_cluster_weight'])
            max_clusters = floor(total_weight / self.min_cluster_weight)

        min_clusters = 2
        if params['max_cluster_weight'] != 'None':
            self.max_cluster_weight = int(params['max_cluster_weight'])
            min_clusters = floor(total_weight / self.max_cluster_weight)
        return floor((max_clusters + min_clusters) / 2)

    def generate_mst(self):
        # return minimum spanning tree from center_matrix
        clusters_distances = pairwise_distances(self.centers)
        self.centers_mst   = shortest_path(clusters_distances)

    def calculate_cluster_weights(self):
        label_a = np.array(self.labels)
        weights_a = np.array(self.sample_weights)
        self.cluster_weights = np.bincount(label_a, weights=weights_a)

    def satisfies_minmax(self):
        for size in self.cluster_weights:
            if ((size < self.min_cluster_weight) or (size > self.max_cluster_weight)):
                return False
        return True

    def find_unbalanced_cluster(self):
        # returns most unbalanced cluster (biggest or smallest) with respect to ideal average weight
        return True

    def rebalance(self, cluster, processed_clusters):
        # recursive
        processed_clusters += [cluster]
        neighbors = self.get_neighbors(cluster, processed_clusters)
        median_weight = self.calculate_median_weight(cluster, neighbors)
        for neighbors in neighbors:
            self.balance(cluster, neighbor, median_weight)
        for neighbors in neighbors:
            self.rebalance(most_unbalanced_cluster, processed_clusters)

    def get_neighbors(self, cluster, processed_clusters):
        # return not processed neighbors
        return True

    def calculate_median_weight(self, cluster, neighbors):
        # return median weight between cluster and neighbors
        return True

    def balance(self, cluster, neighbor, median_weight):
        n = self.weight_to_transfer(cluster, neighbor, median_weight)
        border_points = self.find_border_points(cluster, neighbor, n)
        self.transfer_points(border_points, labels, cluster, neighbor)

    def weight_to_transfer(self, cluster, neighbor, median_weight):
        # returns amount of points to be transferred so that:
        # 1) both clusters end up with same weight
        # 2) clusters end up with a weight equal to median_weight if posible
        return True

    def find_border_points(self, origin_cluster, destiny_cluster, weight):
        border_points = []
        points_distances = [] # [(point, distance_diff),..]
        # ordenar puntos
        origin_cluster_points = [i for i, value in enumerate(self.labels) if value == origin_cluster]
        for point in origin_cluster_points:
            point_coord = np.array([self.data_frame.iloc[point].latitude, self.data_frame.iloc[point].longitude])
            origin_coord = np.array(self.centers[origin_cluster])
            destiny_coord = np.array(self.centers[destiny_cluster])
            distance_diff = abs(cdist(point_coord, origin_coord) - cdist(point_coord, destiny_coord))
            points_distances.append((point, distance_diff))
        # sort de menor a mayor
        points_distances.sort(key = lambda x: x[1])
        # calcular peso hasta n
        current_weight = 0
        for point in points_distances:
            if (current_weight + self.sample_weights[point]) < weight:
                border_points.append(point)
                current_weight += self.sample_weights[point]
        return border_points

    def transfer_points(self, points, origin, destiny):
        # transfer points from origin cluster to destiny cluster
        return True
