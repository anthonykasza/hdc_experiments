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
bin_symbols = make_bins(bins=bins)
bin_ranges = discretize(0, 100, bins)

# for each feature/column make a symbol
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


predicted_labels, centroids, iterations = kbundles(data_symbols, k=2)
print('predictions', predicted_labels)
print('actual labels', targets)
