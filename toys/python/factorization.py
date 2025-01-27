# inspired by resonator networks
#  since bind() is its own inverse this doesn't work great
#  see fractional power encoding
# the script seems to get stuck on 1s and 50s which means i probably
#  have an off-by-one bug somewhere

import random
from utils import hdv, bind, bundle, cossim, make_levels


# make codebooks for 3 variables: x, y, z
# each codebook represents a contiguous vector field
#codebook_size = 10000
codebook_size = 100
x_codebook = make_levels(bins=codebook_size, n=10_000)
y_codebook = make_levels(bins=codebook_size, n=10_000)
z_codebook = make_levels(bins=codebook_size, n=10_000)

# select x, y, and z at random ensuring no zeros
x_idx = random.randint(1, codebook_size)
y_idx = random.randint(1, codebook_size)
z_idx = random.randint(1, codebook_size)

# create the binding to factor
#  minus 1 here to account for the ranges which start at 1
x_hv = x_codebook[x_idx-1]
y_hv = y_codebook[y_idx-1]
z_hv = z_codebook[z_idx-1]
bound_hv = bind(x_hv, y_hv, z_hv)

# create superimposed estimate vectors,
#  guess-and-check all atomic hvs in each code book at once
x_estimate_bundle_hv = bundle(*x_codebook)
y_estimate_bundle_hv = bundle(*y_codebook)
z_estimate_bundle_hv = bundle(*z_codebook)

def find_best_estimate(codebook, est, param2, param3, bound_hv):
  max_sim = cossim(est, bound_hv)
  max_sim_idx = 0
  for idx in range(1, len(codebook)):
    hv = codebook[idx]
    est = bind(bound_hv, param2, param3)
    sim = cossim(hv, est)
    if sim > max_sim:
      max_sim_idx = idx
      max_sim = sim
  return (max_sim, max_sim_idx, codebook[max_sim_idx])

x_max_sim = 0.0
y_max_sim = 0.0
z_max_sim = 0.0
iters = 0
while x_max_sim < 0.1 or y_max_sim < 0.1 or z_max_sim < 0.1:
  iters += 1
  print(iters)

  # find x
  x_max_sim, x_max_sim_idx, x_estimate_bundle_hv = find_best_estimate(
    x_codebook,
    x_estimate_bundle_hv, y_estimate_bundle_hv, z_estimate_bundle_hv,
    bound_hv
  )

  # find y
  y_max_sim, y_max_sim_idx, y_estimate_bundle_hv = find_best_estimate(
    y_codebook,
    y_estimate_bundle_hv, x_estimate_bundle_hv, z_estimate_bundle_hv,
    bound_hv
  )

  # find z
  z_max_sim, z_max_sim_idx, z_estimate_bundle_hv = find_best_estimate(
    z_codebook,
    z_estimate_bundle_hv, x_estimate_bundle_hv, y_estimate_bundle_hv,
    bound_hv
  )

# shift to account for index starting at 1 instead of 0
x_max_sim_idx += 1
y_max_sim_idx += 1
z_max_sim_idx += 1

# the big reveal
print()
print(f'\t\tx * y * z = S')
print(f'selected\t{x_idx} * {y_idx} * {z_idx} = {x_idx*y_idx*z_idx}')
print(f'inferred\t{x_max_sim_idx} * {y_max_sim_idx} * {z_max_sim_idx} = {x_max_sim_idx*y_max_sim_idx*z_max_sim_idx}')

print('cossim(x_hv, x_estimate_bundle_hv)', cossim(x_hv, x_estimate_bundle_hv))
print('cossim(y_hv, y_estimate_bundle_hv)', cossim(y_hv, y_estimate_bundle_hv))
print('cossim(z_hv, z_estimate_bundle_hv)', cossim(z_hv, z_estimate_bundle_hv))

est_bound_hv = bind(x_estimate_bundle_hv, y_estimate_bundle_hv, z_estimate_bundle_hv)
print('cossim(bound_hv, est_bound_hv)', cossim(bound_hv, est_bound_hv))
