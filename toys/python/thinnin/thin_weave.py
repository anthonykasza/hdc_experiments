import numpy as np
import sys; sys.path.insert(0, "../")
from utils import hdv, cossim


def thin(hv):
  '''a very simple 2 element window is slid
     across an HV to make and return a more sparse,
     but similar HV
  '''
  sparse = []
  for idx in range(len(hv)):
    if idx == 0:
      continue
    this_element = hv[idx]
    prev_element = hv[idx-1]
    # -1 followed by -1 results in -1
    if this_element == -1 and prev_element == -1:
      sparse.append(-1)
    # 1 followed by 1 results in 1
    elif this_element == 1 and prev_element == 1:
      sparse.append(1)
    # -1 followed by 1 or 1 followed by -1 results in 0 OR
    #   if either is 0 then 0
    else:
      sparse.append(0)
  # pad the sparse vector
  return np.array([0] + sparse)


def weave(hv):
  '''a very simple 2 element window is slid
     across a sparse HV to make and return a more dense,
     but (potentially more) similar HV
  '''
  dense = []
  for idx in range(len(hv)):
    this_element = hv[idx]
    prev_element = hv[idx-1]
    # 0 followed by -1 results in -1
    if this_element == 0 and prev_element == -1:
      dense.append(-1)
    # 0 followed by 1 results in 1
    elif this_element == 0 and prev_element == 1:
      dense.append(1)
    # do not modify
    else:
      dense.append(hv[idx])
  return np.array(dense)



# Make a dense vector more sparse
original_hv = hdv()
sparse = thin(original_hv)
print(original_hv[:10], original_hv[len(original_hv)-10:])
print(sparse[:10], sparse[len(sparse)-10:])
zero_count = len(sparse) - np.count_nonzero(sparse)
print(cossim(original_hv, sparse), zero_count) # 70% similar to original


# Make the same sparse vector more dense, randomly
dense = weave(sparse)
print(sparse[:10], sparse[len(sparse)-10:])
print(dense[:10], dense[len(dense)-10:])
print(cossim(dense, original_hv)) # 30% similar to original


# Make the same randomly dense vector more sparse, again
sparse = thin(dense)
print( cossim(sparse, original_hv) ) # semi-orthogonal to original




# What would happen if thin() and weave() had adjustable window sizes?
#  i think clip(window.sum()) would be a majority vote
