from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd

def run(data_frame, sample_weights, params):
  eps = 0.015
  if params['eps'] != 'None':
    eps = float(params['eps'])
  min_samples = 5
  if params['min_sample_size'] != 'None':
    min_samples = int(params['min_sample_size'])
  
  #if params['min_max'] == 'True':
    res = minmax(eps, params, sample_weights, data_frame)
    return res
  #else:
    #return DBSCAN(eps, min_samples).fit(data_frame, sample_weight=sample_weights).labels_

def minmax(eps_ini, params, sample_weights, data_frame):
  epsMax = eps_ini * 2
  epsMin = eps_ini / 2
  eps = eps_ini
  min_samples = 600 #int(params['min_cluster_weight'])
 # max = int(params['max_cluster_weight'])
  total_weight = len(data_frame)
  if params['use_weights'] == 'True':
    total_weight = sum(sample_weights)
  result_labels = get_initial_labels(data_frame)

  #iterate with a greater eps
  while (eps < epsMax):
    results = DBSCAN(eps, min_samples).fit(data_frame, sample_weight=sample_weights).labels_
    result_labels = set_labels_in_max(result_labels, results, sample_weights, 5000)
    (data_frame, sample_weights) = remove_already_clusterized_data(result_labels, data_frame, sample_weights)
    eps = eps * 1.1

  eps = eps_ini
  #iterate with a lower eps
  while (eps > epsMin):
    results = DBSCAN(eps, min_samples).fit(data_frame, sample_weight=sample_weights).labels_
    result_labels = set_labels_in_max(result_labels, results, sample_weights, 5000)
    (data_frame, sample_weights) = remove_already_clusterized_data(result_labels, data_frame, sample_weights)
    eps = eps * 0.99
  
  return result_labels

def remove_already_clusterized_data(result_labels, data_frame, sample_weights):
  #keep only the points that are not yet cluterized
  new_data_frame = []
  arr = data_frame.as_matrix()
  new_sample_weights = []
  j = 0
  for i in range(len(result_labels)):
    if result_labels[i] == -1:
      new_sample_weights.append(sample_weights[j])
      new_data_frame.append(arr[j])
      j = j+1
  return (pd.DataFrame(new_data_frame), new_sample_weights)


def get_initial_labels(data_frame):
  labels = []
  for i in data_frame.as_matrix():
    labels.append(-1)
  return labels

def remove_repeated_numbers(elements, num, new_num):
  #assign new numbers for clusters cause in the new iteration some of them could be the same
  new_elements = []
  for e in elements:
    if e == num:
      new_elements.append(new_num)
    else:
      new_elements.append(e)
  return new_elements

def set_labels_in_max(result_labels, result_iter, sample_weights, max_cluster_weight):
  #get cluster numbers taken
  non_available_cluster_number = np.unique(result_labels)
  #get cluster numbers for new interation
  number_of_new_clusters = np.unique(result_iter)
  new_numbers = []
  result_iter = result_iter.tolist()
  for r in number_of_new_clusters:
    if (r != -1 and r in non_available_cluster_number):
      #for each number of cluster repeted, assign a new one
      number_of_new_clusters = np.unique(result_iter)
      next_num = max([*non_available_cluster_number, *number_of_new_clusters, *new_numbers]) + 1
      result_iter = remove_repeated_numbers(result_iter, r, next_num)
      new_numbers.append(next_num)

  label_list = result_iter
  (satisfies, not_satisfies) = satisfies_minmax(label_list, sample_weights, max_cluster_weight)
  #returns cluster numbers that satisfies and dont satisfy max
  k = 0
  res = []
  for i in result_labels:
    if k < len(label_list)+1:
      if i == -1:
        if label_list[k] in satisfies:
          res.append(label_list[k])
        else:
          res.append(-1)
        k = k+1
      else:
        res.append(i)
  return res

def satisfies_minmax(label_list , sample_weights, max_cluster_weight):
  weights_list = sample_weights
  if sample_weights == None:
    weights_list = ([1] * (len(label_list)))
  label_list = np.array(label_list)
  label_list = np.where(label_list == -1, 1000000, label_list) 
  weights_array = np.unique(label_list)
  weights_array = np.where(weights_array == 1000000, -1, weights_array)
  x = np.bincount(label_list, weights = weights_list)
  value_weight_array = x[weights_array]

  #results
  ret_list_ok = []
  ret_list_not_ok = []
  for i in range(len(weights_array)):
    if (value_weight_array[i] > max_cluster_weight):
      ret_list_not_ok.append(weights_array[i])
    else:
      ret_list_ok.append(weights_array[i])
  return (ret_list_ok, ret_list_not_ok)