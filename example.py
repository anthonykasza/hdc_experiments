import numpy as np
from sklearn import datasets
from utils import hdv, bind, bundle
from utils import make_bins, discretize, kmeans


iris = datasets.load_iris()

# bins per feature's range
bins = 100
bins_table = make_bins(bins=bins)


feature_name_symbols = {}
feature_name_bin_symbols = {}
for i, fn in enumerate(iris.feature_names):
  feature_name_symbols[fn] = hdv()
  min_val = np.min(iris.data[:, i])
  max_val = np.max(iris.data[:, i])
  range_list = discretize(min_val, max_val, bins)
  feature_name_bin_symbols[fn] = {}
  for idx in range(len(range_list)):
    feature_name_bin_symbols[fn][range_list[idx]] = bins_table[idx]

# each element of data will be a bundle representing a single sample
data = []
for i, sample in enumerate(iris.data):
  features = []
  for feature_name, value in zip(iris.feature_names, sample):
    f_symbol = feature_name_symbols[feature_name]
    for (start, stop) in feature_name_bin_symbols[feature_name]:
      if value >= start and value <= stop:
        features.append(bind(f_symbol, feature_name_bin_symbols[feature_name][(start, stop)]))
  data.append(bundle(*features))


# predict labels using kbinding
from sklearn.metrics import confusion_matrix
X = iris.data
y = iris.target
predicted_labels, centroids = kmeans(data, k=3)
cm = confusion_matrix(y, predicted_labels)
cluster_to_label = cm.argmax(axis=1)
mapped_cluster_labels = np.array([cluster_to_label[label] for label in predicted_labels])
correct_predictions = np.sum(mapped_cluster_labels == y)
kb_accuracy = correct_predictions / len(y) * 100


# predict labels using traditional kmeans
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X_scaled)
cluster_labels = kmeans.labels_
cm = confusion_matrix(y, cluster_labels)
cluster_to_label = cm.argmax(axis=1)
mapped_cluster_labels = np.array([cluster_to_label[label] for label in cluster_labels])
correct_predictions = np.sum(mapped_cluster_labels == y)
km_accuracy = correct_predictions / len(y) * 100

print(f'hdv predictions \n{predicted_labels}')
print(f'trad kmeans predictions \n{cluster_labels}')
print(f'true labels \n{iris.target}')
print()

print("hdv accuracy", kb_accuracy)
print("kmeans accuracy", km_accuracy)

