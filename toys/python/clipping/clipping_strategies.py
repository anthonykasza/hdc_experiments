
import numpy as np


def new_hv(n=10_000, all=None):
  if all is not None:
    return np.full((1, n), all).flatten()
  group = [-3, -2, -1, 1, 2, 3]
  return np.random.choice(group, size=n)

def cossim(hdv1, hdv2):
  if norm(hdv1) == 0 or norm(hdv2) == 0:
    return 0
  return abs(np.dot(hdv1, hdv2) / (norm(hdv1) * norm(hdv2)))



# Three clipping functions
def clip_sign(hv):
  '''Clip to 1 or -1'''
  return np.sign(hv)

def clip_dec(hv, i=1):
  '''Adjust each element towards 0 by i'''
  for idx in range(len(hv)):
    if hv[idx] > 0:
      hv[idx] = hv[idx] - i
    elif hv[idx] < 0:
      hv[idx] = hv[idx] + i
  return hv

def clip_dec_mean(hv):
  '''Adjust each element towards 0 by the mean'''
  i = int(np.mean(hv))
  for idx in range(len(hv)):
    if hv[idx] > 0:
      hv[idx] = hv[idx] - i
    elif hv[idx] < 0:
      hv[idx] = hv[idx] + i
  return hv



class CountingBundle(object):
  def __init__(self, rate, clip_func, n=10_000):
    self.clip_rate = rate
    self.counter = 0
    self.clip_func = clip_func
    self.value = new_hv(n, all=0)

  def bundle(self, *args):
    '''Clip after some count of accumulated HV'''
    for hv in args:
      self.value += hv
      self.counter += 1
      if self.counter > self.clip_rate:
        self.counter = 0
        self.value = self.clip_func(self.value)
        print('  clipping')


class ThresholdBundle(object):
  def __init__(self, thresh, clip_func, n=10_000):
    self.thresh = thresh
    self.value = new_hv(n, all=0)
    self.clip_func = clip_func

  def bundle(self, *args):
    '''Clip after an element breaches a threshold'''
    for hv in args:
      self.value += hv
      if np.max(self.value) > self.thresh or \
      np.min(self.value) < self.thresh * -1:
        self.value = self.clip_func(self.value)
        print('  clipping')



class BatchBundle(object):
  def __init__(self, clip_func, n=10_000):
    self.value = new_hv(n, all=0)
    self.clip_func = clip_func

  def bundle(self, *args):
    '''Clip after each batch'''
    self.value = self.clip_func(np.sum([hdv for hdv in args], axis=0))
    print('  clipping')



class ExplicitBundle(object):
  def __init__(self, clip_func, n=10_000):
    self.value = new_hv(n, all=0)
    self.clip_func = clip_func

  def bundle(self, *args, clip=False):
    '''Clip when the caller says so'''
    if clip:
      self.value = self.clip_func(np.sum([hdv for hdv in args], axis=0))
    else:
      self.value = np.sum([hdv for hdv in args], axis=0)
