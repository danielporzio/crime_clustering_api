import pulp
import random
import argparse
import numpy as np
import pdb
import math

def l2_distance(point1, point2):
    return sum([(float(i)-float(j))**2 for (i,j) in zip(point1, point2)])

class subproblem(object):
    def __init__(self, centroids, data, weights, min_weight, max_weight):

        self.centroids = centroids
        self.data = data
        self.weights = weights
        self.min_weight = min_weight
        self.max_weight= max_weight
        self.n = len(data)
        self.k = len(centroids)

        self.create_model()

    def create_model(self):
        def distances(assignment):
            return l2_distance(self.data[assignment[0]], self.centroids[assignment[1]])

        assignments = [(i, j) for i in range(self.n) for j in range(self.k)]

        # assignment variables
        self.y = pulp.LpVariable.dicts('data-to-cluster assignments',
                                  assignments,
                                  lowBound=0,
                                  upBound=1,
                                  cat=pulp.LpInteger)

        # create the model
        self.model = pulp.LpProblem("Model for assignment subproblem", pulp.LpMinimize)

        # objective function
        self.model += pulp.lpSum([distances(assignment) * self.weights[assignment[0]] * self.y[assignment] for assignment in assignments]), 'Objective Function - sum weighted squared distances to assigned centroid'
        # this is also weighted, otherwise the weighted centroid computation don't make sense.

        # constraints on the total weights of clusters
        for j in range(self.k):
            self.model += pulp.lpSum([self.weights[i] * self.y[(i, j)] for i in range(self.n)]) >= self.min_weight, "minimum weight for cluster {}".format(j)
            self.model += pulp.lpSum([self.weights[i] * self.y[(i, j)] for i in range(self.n)]) <= self.max_weight, "maximum weight for cluster {}".format(j)

        # make sure each point is assigned at least once, and only once
        for i in range(self.n):
            self.model += pulp.lpSum([self.y[(i, j)] for j in range(self.k)]) == 1, "must assign point {}".format(i)

    def solve(self):
        self.status = self.model.solve()

        clusters = None
        if self.status == 1:
            clusters= [-1 for i in range(self.n)]
            for i in range(self.n):
                for j in range(self.k):
                    if self.y[(i, j)].value() > 0:
                        clusters[i] = j
        return clusters

def initialize_centers(dataset, k):
    """
    sample k random datapoints as starting centers
    """
    ids = list(range(len(dataset)))
    random.shuffle(ids)
    return [dataset[id] for id in ids[:k]]

def compute_centers(clusters, dataset,weights=None):
    """
    weighted average of datapoints to determine centroids
    """
    if weights is None:
        weights = [1]*len(dataset)
    # canonical labeling of clusters
    ids = list(set(clusters))
    c_to_id = dict()
    for j, c in enumerate(ids):
        c_to_id[c] = j
    for j, c in enumerate(clusters):
        clusters[j] = c_to_id[c]

    k = len(ids)
    dim = len(dataset[0])
    cluster_centers = [[0.0] * dim for i in range(k)]
    cluster_weights = [0] * k
    for j, c in enumerate(clusters):
        for i in range(dim):
            cluster_centers[c][i] += dataset[j][i] * weights[j]
        cluster_weights[c] += weights[j]
    for j in range(k):
        for i in range(dim):
            cluster_centers[j][i] = cluster_centers[j][i]/float(cluster_weights[j])
    return clusters, cluster_centers

def minsize_kmeans_weighted(dataset, k, weights=None, min_weight=0, max_weight=None,max_iters=1,uiter=None):
    """
    @dataset - numpy matrix (or list of lists) - of point coordinates
    @k - number of clusters
    @weights - list of point weights, length equal to len(@dataset)
    @min_weight - minimum total weight per cluster
    @max_weight - maximum total weight per cluster
    @max_iters - if no convergence after this number of iterations, stop anyway
    @uiter - iterator like tqdm to print a progress bar.
    """
    n = len(dataset)
    if weights is None:
        weights = [-1]*n
    if max_weight == None:
        max_weight = sum(weights)
    uiter = uiter or list

    centers = initialize_centers(dataset, k)
    clusters = [-1] * n

    for ind in uiter(range(max_iters)):
        m = subproblem(centers, dataset, weights, min_weight, max_weight)
        clusters_ = m.solve()
        if not clusters_:
            return None, None
        clusters_, centers = compute_centers(clusters_, dataset)

        converged = all([clusters[i]==clusters_[i] for i in range(n)])
        clusters = clusters_
        if converged:
            break

    return clusters, centers

def weighted_mm_kmeans(data = [], k=5, weights = [], min_weight = 1, max_weight = 50, numIter = 1):
  best = None
  best_clusters = None
  for i in range(numIter):
    clusters, centers = minsize_kmeans_weighted(data, k, weights,
                                        min_weight, max_weight)
    
  if clusters:
    return clusters
  else:
    print('no clustering found')
    return ([-1] * (len(data)))

def getKforMinMax(min, max, total_weight):
  k_min = total_weight / max
  k_max = total_weight / min
  return (round(k_min), math.floor(k_max))

def main_kmeans_weighted(data_frames, sample_weights, min, max):
  if sample_weights == None:
    weights = ([1] * (len(data_frames)))
  else:
    weights = sample_weights

  data = data_frames.as_matrix()
  new_data = []
  for i in range(len(data)):
    row = []
    for j in range(len(data[i])):
      row.append(data[i][j])
    new_data.append(row)
  (k_min, k_max) = getKforMinMax(min, max, sum(weights))
  for i in range(k_min, k_max):
    print(i)
    res = weighted_mm_kmeans(new_data, i, weights, min, max , 1)
    if res[0] > -1:
      return res
  return res

