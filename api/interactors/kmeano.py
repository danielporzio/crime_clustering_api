from math import floor
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import KMeans
from scipy.sparse.csgraph import shortest_path
import numpy as np

class Kmeano:
    def __init__(self, data_frame, sample_weights):
        self.data_frame         = data_frame
        self.sample_weights     = sample_weights
        self.labels             = None
        self.center_mst         = None
        self.cluster_weights    = None
        self.min_cluster_weight = None
        self.max_cluster_weight = None


    def run(self, params):
        k = self.find_number_of_clusters(params)
        kmeans = KMeans(k).fit(self.data_frame, sample_weight=self.sample_weights)
        centers = kmeans.cluster_centers_
        self.labels = kmeans.labels_
        self.generate_mst(centers)
        self.calculate_cluster_weights()
        while not self.satisfies_minmax():
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
            self.min_cluster_weight = int(params['min_cluster_weight'])
            max_clusters = floor(total_weight / self.min_cluster_weight)

        min_clusters = 2
        if params['max_cluster_weight'] != 'None':
            self.max_cluster_weight = int(params['max_cluster_weight'])
            min_clusters = floor(total_weight / self.max_cluster_weight)
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
        # returns weight to be transferred from cluster to a neighbor
        # or from a neighbor to cluster          
        return abs(self.cluster_weights[cluster] - median_weight)

    def get_neighbors(self, cluster, processed_clusters):
        # return not processed neighbors
        neighbors = []
        for i in range(len(self.center_mst)):
            for j in range(len(self.center_mst)):
                if i == cluster and not(j in processed_clusters) and self.center_mst[i,j] != 0:
                    neighbors.append(j)
        return neighbors

    def calculate_median_weight(self, cluster, neighbors):
        # return median weight between cluster and neighbors
        return True

    def find_border_points(self, cluster, neighbor, n):
        # return x border points that in total weights n to
        # transfer from cluster to neighbor or viceversa
        # depending on which one has bigger size
        return True

    def calculate_cluster_weights(self):
         label_a = np.array(self.labels)
         weights_a = np.array(self.sample_weights)
         self.cluster_weights = np.bincount(label_a,  weights=weights_a)

    def transfer_points(self, points, origin, destiny):
        # transfer points from origin cluster to destiny cluster
        return True

    def generate_mst(self, centers):
        # return minimum spanning tree from center_matrix
        clusters_distances = pairwise_distances(centers)
        self.center_mst = shortest_path(clusters_distances)

    def find_unbalanced_cluster(self):
        # returns most unbalanced cluster (biggest or smallest) with respect to ideal average weight
        return True

    def satisfies_minmax(self):
        for size in self.cluster_weights:
            if size < self.min_cluster_weight:
                return False
            if size > self.max_cluster_weight:
                return False
        return True
