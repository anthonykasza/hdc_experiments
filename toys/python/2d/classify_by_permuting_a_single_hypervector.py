import sys; sys.path.insert(0, '../')
from utils import bind, bundle, cossim, hdv, permute

from collections import defaultdict
from sklearn import datasets
import numpy as np


def embed_image_into_hv(pixels):
  '''Bundle pixel bindings to make an image HV'''
  global THE_ONLY_HV
  global image_x_size
  global image_y_size

  pixel_hvs = []
  for idx, pixel in enumerate(pixels):
    x = int(idx / image_x_size)
    y = idx % image_y_size
    value = int(pixel)

    pixel_x_hv = permute(THE_ONLY_HV, x)
    pixel_y_hv = permute(THE_ONLY_HV, y * -1)

    # i think all of these do the same thing
    #magic = x * y * value
    #magic = (x * value) + (y * value)
    #magic = (x**2) * y + value
    magic = x + y + value
    pixel_value_hv = permute(THE_ONLY_HV, magic)

    pixel_binding = bind(pixel_x_hv, pixel_y_hv, pixel_value_hv)
    pixel_hvs.append(pixel_binding)

  return bundle(*pixel_hvs)


def split_data(data, train_size):
  n = len(data)
  train_idx = np.random.choice(n, size=int(train_size * n), replace=False)
  test_idx = np.setdiff1d(np.arange(n), train_idx)
  return train_idx, test_idx


image_x_size = 8
image_y_size = 8

dims = 10000

# The only hypervector we use to encode images
THE_ONLY_HV = hdv(dims)


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

  r = abs(predictions[closest_fit] - predictions[farthest_fit])
  if closest_fit != label:
    print(f'truth: {label}, predicted: {closest_fit}, range: {r}')
    for k,v in predictions.items():
      print(f'{k}: {v}')
    print()
    wrong_per_class[label] += 1
  else:
    correct_per_class[label] += 1



# These are pretty decent results :)
print(f'trained {dict(sorted(example_count_per_class.items()))}')
print(f'correct {dict(sorted(correct_per_class.items()))}')
print(f'wrong {dict(sorted(wrong_per_class.items()))}')