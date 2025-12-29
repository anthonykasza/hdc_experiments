# I'm not sure the ideas in this script are worth pursuing

import numpy as np
from utils import hdv_real as new_hv


dims = 10000
a = new_hv(dims)
print(f'hv: {a[0:3]}..{a[-3:]}')
print(f'mean: {np.mean(a)}')
print(f'var: {np.var(a)}')
print(f'dims: {len(a)}')
print()

# To visualize this operation, imagine a rubberband.
# It's thickness is the variance of the HV. Increasing the
# dims in this way stretches the band, making it
# thinner in different locations. But, the total mass of
# the band, the HV's mean, doesn't change.
def increase_dimensions(hv, more_dims):
  ''' Split element values to create additional elements.
      Do so in a way which approximately preserves the
      mean and variance of a HV.
  '''
  new_hv = list(hv)
  for idx in range(len(new_hv)):
    while new_hv[idx] != 1 and new_hv[idx] != -1:
      if more_dims == 0:
        return np.array(new_hv)
      more_dims -= 1

      # If the element is negative, add 1 to it
      # and append a -1 element to the end of new hv
      if new_hv[idx] < 0:
        new_hv[idx] += 1
        new_hv.append(-1)

      # If the element is positive, sub 1 from it
      # and append a 1 element to the end of new hv
      elif new_hv[idx] > 0:
        new_hv[idx] -= 1
        new_hv.append(1)


more_dims = 1000
new_a = increase_dimensions(a, more_dims)
print(f'hv: {new_a[0:3]}..{new_a[-3:]}')
print(f'mean: {np.mean(new_a)}')
print(f'var: {np.var(new_a)}')
print(f'dims: {len(new_a)}')



# TODO
class NotUh(Exception):
  def __init__(self):
    pass

def decrease_dimensions(hv, less_dims):
  ''' Merge element values to reduce the count of elements
      Do so in a way which approximately preserves the
      mean and variance of a HV.
  '''
  if len(hv) - less_dims < 0:
    raise NotUh
  bounds = ( np.min(hv), np.max(hv) )
  # Find and remove elements with values of 0.
  # the number of zeros in the hv is greater than the
  # desired less_dims, no further action is taken.
  # Otherwise...
  # Add 2 element values together then drop one of the elements.
  # Do so in a way that ensures no single element's value
  # exceeds the existing max/min values (bounds) of the HV


# TODO - How can we compare vectors of differing lengths?
# TODO - See MBAT. How do decrease_dimensions() and increasee_dimensions()
# compare to matrix multiplication as a binding/resizing operation?
