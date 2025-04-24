import copy
import numpy as np

def new_hv(n=10_000):
  # -5 to 5
  r = [i for i in range(5, -6, -1) if i != 0]
  return np.random.choice(r, size=n)

def add_hv(*args):
  return np.sum([hv for hv in args], axis=0)

def sub_hv(*args):
  return args[0] - np.sum([hv for hv in args[1:]], axis=0)

def compare_hv(hv1, hv2):
  if np.linalg.norm(hv1) == 0 or np.linalg.norm(hv2) == 0:
    return 0
  return abs(np.dot(hv1, hv2) / (np.linalg.norm(hv1) * np.linalg.norm(hv2)))
