
import numpy as np
from numpy.linalg import norm


def new_symbol(n):
  return np.random.choice([5,4,3,2,1, -1,-2,-3,-4,-5], size=n)

def inverse(hv):
  '''Inverse the elements'''
  return np.array([x * -1 for x in hv])

def bundle(*args):
  '''Element-wise addition on even indices'''
  summed = np.sum(args, axis=0)
  result = np.zeros_like(summed)
  result[::2] = summed[::2]
  return result

def sim(hdv1, hdv2):
  '''Similarity'''
  if norm(hdv1) == 0 or norm(hdv2) == 0:
    return 0
  return abs(np.dot(hdv1, hdv2) / (norm(hdv1) * norm(hdv2)))



def cyclic_permute(hdv, shift=1, mode="all"):
  '''Shift permute'''
  result = hdv.copy()

  if mode == "all":
    result = np.roll(hdv, shift)
  elif mode == "even":
    idx = np.arange(0, hdv.size, 2)
    result[idx] = np.roll(hdv[idx], shift)
  elif mode == "odd":
    idx = np.arange(1, hdv.size, 2)
    result[idx] = np.roll(hdv[idx], shift)

  return result
