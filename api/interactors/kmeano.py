from math import floor
from sklearn.cluster import KMeans
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
            processed_clusters = []
            most_unbalanced_cluster = self.find_unbalanced_cluster()
            self.rebalance(most_unbalanced_cluster, processed_clusters)
            i += 1
        return self.labels

    def find_number_of_clusters(self, params):
        total_weight = len(self.data_frame)
        if params['use_weights'] == 'True':
            total_weight = sum(self.sample_weights)

        max_clusters = 50
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
            for possible_neighbour in range(cluster + 1, number_of_clusters):
                distances = cdist(clusters_points[cluster], clusters_points[possible_neighbour])
                if distances.min() < epsilon:
                    adjacency[cluster, possible_neighbour] = 1
                    adjacency[possible_neighbour, cluster] = 1

        clusters_wo_neighbours = np.where(~adjacency.any(axis=1))[0]
        for cluster in clusters_wo_neighbours:
            neighbour = self.nearest_cluster_center(cluster)
            adjacency[cluster, neighbour] = 1
        self.adjacency = adjacency

    def nearest_cluster_center(self, cluster):
        centroid_distances = cdist([self.centers[cluster]], self.centers)
        minimum_distance = np.partition(centroid_distances[0], 1)[1]
        return centroid_distances[0].tolist().index(minimum_distance)

    def calculate_cluster_weights(self):
        label_a = np.array(self.labels)
        weights_a = np.array(self.sample_weights)
        self.cluster_weights = np.bincount(label_a, weights=weights_a)

    def satisfies_minmax(self):
        for size in self.cluster_weights:
            if (( self.min_cluster_weight != None and size < self.min_cluster_weight) or
                ( self.max_cluster_weight != None and size > self.max_cluster_weight )):
                return False
        return True

    def find_unbalanced_cluster(self):
        # returns most unbalanced cluster (biggest or smallest) with respect to ideal average weight
        total_weight = sum(self.cluster_weights)
        average_weight = total_weight / len(self.cluster_weights)
        diff_arr = list(map(lambda x: abs(average_weight - x), self.cluster_weights))
        return diff_arr.index(max(diff_arr))

    def rebalance(self, origin, processed_clusters):
        for cluster in self.clusters_by_distance(origin):
            processed_clusters += [cluster]
            neighbors = self.get_neighbors(cluster, processed_clusters)
            for neighbor in neighbors:
                self.balance(cluster, neighbor)

    def clusters_by_distance(self, cluster):
        clusters_path = []
        centroid_distances = cdist([self.centers[cluster]], self.centers)
        for distance in np.sort(centroid_distances[0]):
            clusters_path += [centroid_distances[0].tolist().index(distance)]
        return clusters_path


    def get_neighbors(self, cluster, processed_clusters):
        # return not processed neighbors
        neighbors = []
        adjacent_clusters = self.adjacency[cluster]
        for i in range(len(self.adjacency)):
            if not(i in processed_clusters) and adjacent_clusters[i] == 1:
                neighbors.append(i)
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
        points_distances = []
        origin_cluster_points = [i for i, value in enumerate(self.labels) if value == origin_cluster]
        for point in origin_cluster_points:
            point_coord = np.array([self.data_frame.iloc[point].latitude, self.data_frame.iloc[point].longitude])
            destiny_center_coord = np.array(self.centers[destiny_cluster])
            distance_diff = cdist([point_coord], [destiny_center_coord])
            points_distances.append((point, distance_diff[0][0]))

        # Avoid cdist multiple times
        # cluster_points_coordinates = self.clusters_points[origin_cluster]
        # destiny_center_coord = np.array(self.centers[destiny_cluster])
        # distances_to_center = cdist(cluster_points_coordinates, [destiny_center_coord])
        # for i in range(len(origin_cluster_points)):
        #     points_distances.append((origin_cluster_points[i], distances_to_center[i][0]))

        points_distances.sort(key = lambda x: x[1])
        current_weight = 0
        for point in points_distances:
            if (current_weight + self.sample_weights[point[0]]) < weight:
                border_points.append(point[0])
                current_weight += self.sample_weights[point[0]]
        return border_points

    def transfer_points(self, points, destiny):
        # transfer points from origin cluster to destiny cluster
        for index in points:
            self.labels[index] = destiny
        self.calculate_cluster_weights()
