# Thank you!
#  https://github.com/mlpotter/Hyperdimensional_Character_Recognition/


import sys; sys.path.insert(0, '../')
from utils import bind, bundle, cossim, hdv, permute

from collections import defaultdict
from sklearn import datasets
import numpy as np
import copy


def embed_image_into_hv(pixels):
  '''Bundle pixel bindings to make an image HV'''
  global x_hv
  global y_hv
  global value_hv

  pixel_hvs = []
  for idx, pixel in enumerate(pixels):
    x = int(idx / 8)
    y = idx % 8
    value = int(pixel)

    # permute everything. no codebooks
    pixel_x_hv = permute(x_hv, x)
    pixel_y_hv = permute(y_hv, y)
    pixel_value_hv = permute(value_hv, value)

    pixel_binding = bind(pixel_x_hv, pixel_y_hv, pixel_value_hv)
    pixel_hvs.append(pixel_binding)

  return bundle(*pixel_hvs)


def split_data(data, train_size):
  n = len(data)
  train_idx = np.random.choice(n, size=int(train_size * n), replace=False)
  test_idx = np.setdiff1d(np.arange(n), train_idx)
  return train_idx, test_idx


dims = 10000

# static hv, 1 for each feature
x_hv = hdv(dims)
y_hv = hdv(dims)
value_hv = hdv(dims)

# Load data
digits = datasets.load_digits()
images = digits.data
labels = digits.target
train_indices, test_indices = split_data(images, train_size=0.8)

# train
examples_per_class = {k:[] for k in range(10)}
example_count_per_class = defaultdict(int)
for idx in train_indices:
  image = images[idx]
  label = int(labels[idx])
  image_hv = embed_image_into_hv(image)

  # TODO - retrain on a sample until it's similarity to
  #        incorrect class centroid HVs decreases to an
  #        acceptable ratio
  examples_per_class[label].append(image_hv)
  example_count_per_class[label] += 1

class_centroids = {}
for label in examples_per_class:
  class_centroids[label] = bundle(*examples_per_class[label])


# test
wrong_per_class = defaultdict(int)
correct_per_class = defaultdict(int)
for idx in test_indices:
  idx = int(idx)
  image = images[idx]
  label = int(labels[idx])
  image_hv = embed_image_into_hv(image)

  predictions = {idx: cossim(image_hv,class_centroids[idx]) for idx in range(len(class_centroids))}
  closest_fit = max(predictions, key=predictions.get)
  farthest_fit = min(predictions, key=predictions.get)

  # why are the prediction ranges so tight? i would think
  #  they should have a much larger range
  r = abs(predictions[closest_fit] - predictions[farthest_fit])

  if closest_fit != label:
    print(f'truth: {label}, predicted: {closest_fit}, range: {r}')
    for k,v in predictions.items():
      print(f'{k}: {v}')
    print()
    wrong_per_class[label] += 1
  else:
    correct_per_class[label] += 1

# These are pretty awful results :(
print(f'trained {dict(sorted(example_count_per_class.items()))}')
print(f'correct {dict(sorted(correct_per_class.items()))}')
print(f'wrong {dict(sorted(wrong_per_class.items()))}')
