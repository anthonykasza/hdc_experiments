# Comparing the results of non-deterministic code
#  is a real pain in the (grand) wazoo. You can't test
#  for values you must test for ranges.


import sys; sys.path.insert(0, '../')
from utils import bind, bundle, cossim, sub, hdv

from collections import defaultdict
from sklearn import datasets
import numpy as np
import copy


def make_levels(steps, hv1=hdv(), hv2=hdv()):
  '''Make non-linear levels'''
  levels = []
  levels.append(hv1)
  step_counter = 0
  start = 0
  total_changed_elements = 0

  while step_counter < len(steps):
    levels.append( copy.deepcopy(levels[len(levels)-1]) )

    elements = int(steps[step_counter] * (len(hv1) / sum(steps)))
    total_changed_elements = total_changed_elements + elements

    levels[len(levels)-1][start:start+elements] = hv2[start:start+elements]
    start = start + elements;
    step_counter = step_counter + 1

  return levels


def value_lookup(value, codebook, steps):
  start = 0
  for idx in range(len(steps)):
    step = steps[idx]
    stop = start + step
    if value > start and value <= stop:
      return codebook[idx]
    start = start + step
  return codebook[-1]


def embed_image_into_hv(pixels):
  '''Bundle pixel bindings to make an image HV'''
  pixel_hvs = []
  for idx, pixel in enumerate(pixels):
    x = int(idx / 8)
    y = idx % 8
    value = int(pixel)

    pixel_x_hv = pixel_x_codebook[x]
    pixel_y_hv = pixel_y_codebook[y]
    pixel_value_hv = pixel_value_codebook[value]

    # uncomment to test with non-linear leveling
    '''pixel_value_hv = value_lookup(value, pixel_value_codebook, pixel_value_steps)'''

    pixel_binding = bind(pixel_x_hv, pixel_y_hv, pixel_value_hv)
    pixel_hvs.append(pixel_binding)

  return bundle(*pixel_hvs)


def split_data(data, train_size):
  n = len(data)
  train_idx = np.random.choice(n, size=int(train_size * n), replace=False)
  test_idx = np.setdiff1d(np.arange(n), train_idx)
  return train_idx, test_idx


dims = 10000

# Leveled Codebooks, these don't work as well as uncorrelated codebooks
'''
pixel_value_codebook = sub(hdv(dims), hdv(dims), 17-1)
pixel_x_codebook = sub(hdv(dims), hdv(dims), 8-1)
pixel_y_codebook = sub(hdv(dims), hdv(dims), 8-1)
'''

# Non-linear Leveled Codebooks, these increase the range of the
#  predictions (confidence) but they still don't perform as well as
#  uncorrelated.
# i played with a few different step strategies but they all seemed
#  worse than random codebooks
'''
pixel_value_steps = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
pixel_value_steps = [500, 500, 500, 500, 500]
pixel_value_steps = [8, 1, 8]
pixel_value_steps = [10, 5, 10]
pixel_value_steps = [1, 3, 2, 1, 1, 2, 3, 1]
pixel_value_steps = [1, 3, 10, 3, 1]
pixel_value_codebook = make_levels(pixel_value_steps)
'''

# Random Uncorrelated Codebooks
pixel_value_codebook = [hdv(dims) for x in range(17)]
pixel_x_codebook = [hdv(dims) for x in range(8)]
pixel_y_codebook = [hdv(dims) for x in range(8)]

# Load data
digits = datasets.load_digits()
images = digits.data
labels = digits.target
# TODO - try different train/test ratios
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
