from math import floor
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import KMeans
from scipy.sparse.csgraph import shortest_path
import numpy as np
import pdb
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
        self.adjacency          = None
        self.cluster_weights    = None
        self.min_cluster_weight = None
        self.max_cluster_weight = None
        self.clusters_points    = None


    def run(self, params):
        k             = self.find_number_of_clusters(params)
        kmeans_output = KMeans(k).fit(self.data_frame, sample_weight=self.sample_weights)
        self.centers  = kmeans_output.cluster_centers_
        self.labels   = kmeans_output.labels_
        self.generate_adjacency_matrix()
        self.calculate_cluster_weights()
        i = 0
        while not self.satisfies_minmax() and i < 1000:
            print('Iteracion - ', i)
            processed_clusters      = []
            self.calculate_cluster_weights()
            most_unbalanced_cluster = self.find_unbalanced_cluster()
            self.rebalance(most_unbalanced_cluster, processed_clusters)
            i = i + 1
        return self.labels

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

    def generate_adjacency_matrix(self):
        # returns adjacency matrix of clusters
        epsilon = 0.01
        number_of_clusters = len(self.centers)
        adjacency = np.zeros((number_of_clusters, number_of_clusters))
        clusters_points = {}
        for cluster in range(number_of_clusters):
            points_indexes = np.where(self.labels == cluster)
            clusters_points[cluster] = np.asmatrix(self.data_frame)[points_indexes]
        self.clusters_points = clusters_points

        for cluster in range(number_of_clusters):
            for possible_neighbour in range(number_of_clusters):
                if cluster != possible_neighbour:
                    distances = cdist(clusters_points[cluster], clusters_points[possible_neighbour])
                    if distances.min() < epsilon:
                        adjacency[cluster, possible_neighbour] = 1
        # agregar caso en que un cluster quede sin vecinos
        # sabemos que los clusters tienen que tener siempre como vecino a su cluster
        # mas cercano
        self.adjacency = adjacency

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
        total_weight = sum(self.cluster_weights)
        average_weight = total_weight / len(self.cluster_weights)
        diff_arr = list(map(lambda x: abs(average_weight - x), self.cluster_weights))
        max_index = diff_arr.index(max(diff_arr))
        return max_index

    def rebalance(self, cluster, processed_clusters):
        # recursive
        processed_clusters += [cluster]
        neighbors = self.get_neighbors(cluster, processed_clusters)
        for neighbor in neighbors:
            self.balance(cluster, neighbor)
        for neighbor in neighbors:
            self.rebalance(neighbor, processed_clusters)

    def get_neighbors(self, cluster, processed_clusters):
        # return not processed neighbors
        neighbors = []
        for i in range(len(self.adjacency)):
            for j in range(len(self.adjacency)):
                if i == cluster and not(j in processed_clusters) and self.adjacency[i,j] == 1:
                    neighbors.append(j)
        return neighbors

    def balance(self, cluster, neighbor):
        average_weight = (self.cluster_weights[cluster] + self.cluster_weights[neighbor]) / 2
        if self.cluster_weights[cluster] > self.cluster_weights[neighbor]:
            origin = cluster
            destiny = neighbor
        else:
            origin = neighbor
            destiny = cluster
        weight_to_transfer = self.cluster_weights[origin] - average_weight
        border_points = self.find_border_points(origin, destiny, weight_to_transfer)
        self.transfer_points(border_points, destiny)

    def find_border_points(self, origin_cluster, destiny_cluster, weight):
        border_points = []
        points_distances = [] # [(point, distance_diff),..]
        # ordenar puntos
        origin_cluster_points = [i for i, value in enumerate(self.labels) if value == origin_cluster]
        # origin_cluster_points = self.clusters_points[origin_cluster]
        for point in origin_cluster_points:
            point_coord = np.array([self.data_frame.iloc[point].latitude, self.data_frame.iloc[point].longitude])
            # origin_coord = np.array(self.centers[origin_cluster])
            destiny_coord = np.array(self.centers[destiny_cluster])
            # distance_diff = abs(cdist([point_coord], [origin_coord]) - cdist([point_coord], [destiny_coord]))
            distance_diff = cdist([point_coord], [destiny_coord])
            points_distances.append((point, distance_diff[0][0]))
        # sort de menor a mayor
        points_distances.sort(key = lambda x: x[1])
        print(points_distances[0], points_distances[len(points_distances)-1])
        # calcular peso hasta n
        current_weight = 0
        for point in points_distances:
            if (current_weight + self.sample_weights[point[0]]) < weight:
                border_points.append(point[0])
                current_weight += self.sample_weights[point[0]]
        return border_points

    def transfer_points(self, points, destiny):
        # transfer points from origin cluster to destiny cluster
        new_labels = self.labels
        for index in points:
            new_labels[index] = destiny
        self.labels = new_labels
        self.calculate_cluster_weights()
