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

  # noise
  [25, 75],
  [70, 30],
]
targets = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, -1, -1]

combined = list(zip(data, targets))
random.shuffle(combined)
data, targets = zip(*combined)
data = list(data)
targets = list(targets)

bins = 10
bin_symbols = make_bins(bins=bins)
bin_ranges = discretize(0, 100, bins)

# for each (2) features make a symbol representing a key
f1_key_symbol = hdv()
f2_key_symbol = hdv()

data_symbols = []
for idx in range(len(data)):
  [f1, f2] = data[idx]
  for (start, stop), bin_symbol in zip(bin_ranges, bin_symbols):

    # for each feature (2) map the feature's value to the range
    #  it is between. then bind that range's symbol with the feature's
    #  key symbol
    if f1 > start and f1 < stop:
      f1_symbol = bind(f1_key_symbol, bin_symbol)
    if f2 > start and f2 < stop:
      f2_symbol = bind(f2_key_symbol, bin_symbol)

  # bundle all (2) the feature symbols together into a single symbol
  #  which represents the entire row of features
  sample_symbol = bundle(f1_symbol, f2_symbol)
  data_symbols.append(sample_symbol)


predicted_labels, centroids, iterations = kbundles(data_symbols, k=3)
print('predictions', predicted_labels)
print('actual labels', targets)
