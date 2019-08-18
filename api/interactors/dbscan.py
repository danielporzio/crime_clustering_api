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

def minmax(eps, params, sample_weights, data_frame):
  min_samples = 400 #int(params['min_cluster_weight'])
 # max = int(params['max_cluster_weight'])
  total_weight = len(data_frame)
  if params['use_weights'] == 'True':
    total_weight = sum(sample_weights)
  satisfies = False
  result_labels = get_initial_labels(data_frame)
  iter = 0
  while (not satisfies and iter < 2):
    results = DBSCAN(eps, min_samples).fit(data_frame, sample_weight=sample_weights).labels_
    result_labels = set_labels_in_max(result_labels, results, sample_weights, 2000)
    (data_frame, sample_weights) = remove_already_clusterized_data(result_labels, data_frame, sample_weights)
    eps = eps * 0.99
    iter = iter + 1
  
  return result_labels

def remove_already_clusterized_data(result_labels, data_frame, sample_weights):
  new_data_frame = []
  arr = data_frame.as_matrix()
  new_sample_weights = []
  for i in range(len(result_labels)):
    if result_labels[i] == -1:
      new_sample_weights.append(sample_weights[i])
      new_data_frame.append(arr[i])
  
  return (pd.DataFrame(new_data_frame), new_sample_weights)


def get_initial_labels(data_frame):
  labels = []
  for i in data_frame.as_matrix():
    labels.append(-1)
  return labels

def set_labels_in_max(result_labels, result_iter, sample_weights, max_cluster_weight):
  next_available_cluster_number = max(np.unique(result_labels)) + 1
  print(next_available_cluster_number)
  ##para cada elem en las labels del result iter, obtener cuales son los numers
  # de los clusters, y ponerles numeros mayores al next_available_cluster_number
  # asi no se confunden con los clusters ya formados
  # una vez esto sigo cn los siguientes pasos
  label_list = result_iter.tolist()
  (satisfies, not_satisfies) = satisfies_minmax(label_list, sample_weights, max_cluster_weight)
  #returns cluster numbers that satisfies and dont satisfy max
  k = 0
  res = []
  for i in result_labels:
    if k < len(label_list):
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