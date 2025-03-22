# 8x8 pixel images
# values are b/w, 0 through 16
# each image is 1 of 10 categories, 0 through 9


import sys; sys.path.insert(0, '../')
from utils import bind, bundle, cossim, sub, hdv

from collections import defaultdict
from sklearn import datasets
import numpy as np


def embed_image_into_hv(pixels):
  '''Bundle pixel bindings to make an image HV'''
  pixel_hvs = []
  for idx, pixel in enumerate(pixels):

    # this could very easily be expanded to
    #  support RBG values as well as more
    #  dimensions than 2. CT scans would be neat to try

    value = int(pixel)
    x = int(idx / 8)
    y = idx % 8

    pixel_value_hv = pixel_value_codebook[value]
    pixel_x_hv = pixel_x_codebook[x]
    pixel_y_hv = pixel_y_codebook[y]

    pixel_binding = bind(pixel_x_hv, pixel_y_hv, pixel_value_hv)
    pixel_hvs.append(pixel_binding)

  return bundle(*pixel_hvs)


def split_data(data, train_size):
  n = len(data)
  train_idx = np.random.choice(n, size=int(train_size * n), replace=False)
  test_idx = np.setdiff1d(np.arange(n), train_idx)
  return train_idx, test_idx


# there's likely a sweet spot for this
dims = 10000

# Why do random uncorrelated codebooks produce better
#  results than leveled codebooks?
# TODO - try non linear leveling for the pixel_value_codebook

# Leveled Codebooks
#pixel_value_codebook = sub(hdv(dims), hdv(dims), 17-1)
#pixel_x_codebook = sub(hdv(dims), hdv(dims), 8-1)
#pixel_y_codebook = sub(hdv(dims), hdv(dims), 8-1)

# Random Uncorrelated Codebooks
pixel_value_codebook = [hdv(dims) for x in range(17)]
pixel_x_codebook = [hdv(dims) for x in range(8)]
pixel_y_codebook = [hdv(dims) for x in range(8)]


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

  # TODO - consider retraining with an image_hv based on its
  #        cossim to incorrect class bundles
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
  #  they should have a much larger difference
  r = abs(predictions[closest_fit] - predictions[farthest_fit])

  if closest_fit != label:
    print(f'truth: {label}, predicted: {closest_fit}, range: {r}')
    for k,v in predictions.items():
      print(f'{k}: {v}')
    print()
    wrong_per_class[label] += 1
  else:
    correct_per_class[label] += 1

# These are pretty awful results
print(f'trained {dict(sorted(example_count_per_class.items()))}')
print(f'correct {dict(sorted(correct_per_class.items()))}')
print(f'wrong {dict(sorted(wrong_per_class.items()))}')
