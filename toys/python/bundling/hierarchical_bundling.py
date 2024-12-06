import numpy as np
from numpy.linalg import norm

def new_hv(n=10_000):
  return np.random.choice([5,4,3,2,1, -1,-2,-3,-4,-5], size=n)

def clip(hv):
  return np.sign(hv)

def bundle(*args):
  return np.sum([hdv for hdv in args], axis=0)

def cossim(hv1, hv2):
  if norm(hv1) == 0 or norm(hv2) == 0:
    return 0
  return abs(np.dot(hv1, hv2) / (norm(hv1) * norm(hv2)))


# Without clipping, addition is commutative.
# Bundle 10 HV at a time, then bundle 10 superposed HVs into
#  a single HV
atoms = [new_hv() for x in range(100)]
groups = []
for i in range(10):
  groups.append(bundle(*atoms[10*i : 10*(i+1)]))

hierarch_bundle = bundle(*groups)
regular_bundle = bundle(*atoms)
print('clipping only after all bundling is completed')
print( cossim(hierarch_bundle, regular_bundle) )
print()

# Be careful when to clip
# Bundle 10 HV at a time, then clip, then bundle those
#  10 clipped HVs into a single HV
# NOTE: the effects of clipping between bundles is more
#       pronounced for real-valued elements than for binary
atoms = [new_hv() for x in range(100)]
groups = []
for i in range(10):
  groups.append(clip(bundle(*atoms[10*i : 10*(i+1)])))

hierarch_bundle = bundle(*groups)
regular_bundle = bundle(*atoms)
print('clipping after each batch of 10')
print( cossim(hierarch_bundle, regular_bundle) )
