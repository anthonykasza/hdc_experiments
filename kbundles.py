import numpy as np
from sklearn import datasets
from utils import hdv, bind, bundle
from utils import make_bins, discretize, kbundles

iris = datasets.load_iris()


# Make symbolic ranges for all features
features_range_symbols = {}

# all feature dimensions will use the same number of partitions, 100
bins_per_feature = [100] * len(iris.feature_names)
# one could use a different number of buckets per feature
#  bins_per_feature = [100, 50, 100, 50]
for feature_idx, feature_name in enumerate(iris.feature_names):
  features_range_symbols[feature_idx] = {}
  bins_for_this_feature = bins_per_feature[feature_idx]
  bin_symbols = make_bins(bins=bins_for_this_feature)
  bin_ranges = discretize(
    min_val=np.min(iris.data[:, feature_idx]),
    max_val=np.max(iris.data[:, feature_idx]),
    bins=bins_for_this_feature
  )
  for (start, stop), symbol in zip(bin_ranges, bin_symbols):
    features_range_symbols[feature_idx][start, stop] = symbol

'''
features_range_symbols = {
  [0] = {
    (0.0, 0.1) = hdv()
    (0.1, 0.2) = hdv()
    (0.2, 0.3) = hdv()
  },
  [1] = {
    (2.3, 2.7) = hdv()
    (2.7, 3.1) = hdv()
    (3.1, 3.5) = hdv()
    ...
  },
  [2] = { ... }
  [3] = { ... }
 }
'''

# make a list of bundles representing each sample
data_symbols = []
for sample_idx, sample in enumerate(iris.data):
  sample_feature_symbols = []
  for feature_idx in range(len(sample)):
    value = sample[feature_idx]
    for start, stop in features_range_symbols[feature_idx]:
      range_symbol = features_range_symbols[feature_idx][start, stop]
      if value >= start and value <= stop:
        # what happens if we made too many ranges and start/stop are equal?
        sample_feature_symbols.append(range_symbol)
  data_symbols.append( bundle(*sample_feature_symbols) )



# compare kbundle to traditional kmeans
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
X = iris.data
y = iris.target

# predict labels using kbundles
predicted_labels, centroids, iterations = kbundles(data_symbols, k=3)
cm = confusion_matrix(y, predicted_labels)
cluster_to_label = cm.argmax(axis=1)
mapped_cluster_labels = np.array([cluster_to_label[label] for label in predicted_labels])
correct_predictions = np.sum(mapped_cluster_labels == y)
kb_accuracy = correct_predictions / len(y) * 100
kb_precision = precision_score(y, mapped_cluster_labels, average='weighted', zero_division=0)
kb_recall = recall_score(y, mapped_cluster_labels, average='weighted', zero_division=0)
kb_f1 = f1_score(y, mapped_cluster_labels, average='weighted', zero_division=0)


# predict labels using traditional kmeans
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
km_precision = precision_score(y, mapped_cluster_labels, average='weighted', zero_division=0)
km_recall = recall_score(y, mapped_cluster_labels, average='weighted', zero_division=0)
km_f1 = f1_score(y, mapped_cluster_labels, average='weighted', zero_division=0)

print(f'kbundles\n{np.array(predicted_labels)}')
print(f'kmeans\n{cluster_labels}')
print(f'ground truth\n{iris.target}')
print()

print("kb")
print("  accuracy", kb_accuracy)
print("  precision", kb_precision)
print("  recall", kb_recall)
print("  f1", kb_f1)

print("km")
print("  accuracy", km_accuracy)
print("  precision", km_precision)
print("  recall", km_recall)
print("  f1", km_f1)
