import sys; sys.path.insert(0, "../")
from utils import *
import random

data = [
  # cluster 0's points are near 0,0
  [11, 7],
  [2, 13],
  [7, 1],
  [4, 9],
  [3, 5],

  # cluster 1's points are near 100,100
  [86, 94],
  [99, 98],
  [90, 85],
  [99, 94],
  [91, 98],

  # cluster 2's points are in the middle
  [50, 50],
  [51, 52],
  [48, 54],

  # noise, but kmeans doesn't handle noise, so cluster 2
  [25, 76],
  [70, 30],
]
targets = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, -1, -1]

bins = 10
bin_symbols = make_levels(bins=bins)
bin_ranges = discretize(min_val=0, max_val=100, bins=bins)

data_symbols = []
for idx in range(len(data)):
  [feature1, feature2] = data[idx]
  for (start, stop), bin_symbol in zip(bin_ranges, bin_symbols):
    if feature1 > start and feature1 < stop:
      feature1_symbol = bin_symbol
    if feature2 > start and feature2 < stop:
      feature2_symbol = bin_symbol

  sample_symbol = bind(feature1_symbol, feature2_symbol)
  data_symbols.append(sample_symbol)

'''
print("similarity matrix")
similarity_matrix = []
for i in range(len(data)):
  similarity_matrix.append([])
  for j in range(len(data)):
    similarity_matrix[i].append(round( cossim(data[i], data[j]), 2 ))
for row in similarity_matrix:
  print(row)
'''

# kbundles
predicted_labels, centroids, iterations = kbundles(data, k=3)


# traditional kmeans
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(data)
kmeans = KMeans(n_clusters=3, init='random')
kmeans.fit(X_scaled)
kmeans.labels_

# how'd it go?
print(f'targets, {targets}')
print(f'kbundles, {predicted_labels}')
print(f'kmeans, {kmeans.labels_}')
