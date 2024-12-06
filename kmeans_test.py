from utils import *

data = [
  # cluster 0's points are near 0,0
  [1, 1],
  [1, 2],
  [3, 1],
  [1, 2],
  [2, 3],

  # cluster 1's points are near 100,100
  [99, 94],
  [99, 98],
  [97, 99],
  [99, 94],
  [98, 98],
]
targets = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
bins = 10
bin_table = make_bins(bins=bins)
bin_ranges = discretize(0, 100, bins)
bin_range_symbols = dict(zip(bin_ranges, bin_table))

data_symbols = []
for idx in range(len(data)):
  [f1, f2] = data[idx]
  for bin_range,range_symbol in bin_range_symbols.items():
    start, stop = bin_range[0], bin_range[1]
    if f1 > start and f1 < stop:
      f1_symbol = range_symbol
    if f2 > start and f2 < stop:
      f2_symbol = range_symbol
  sample_symbol = bind(f1_symbol, f2_symbol)
  data_symbols.append(sample_symbol)

predicted_labels, centroids = kmeans(data, k=2)
print('predictions', predicted_labels)
print('actual labels', targets)
