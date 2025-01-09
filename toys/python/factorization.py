# inspired by resonator networks
#  since bind() is its own inverse this doesn't work great
#  see fractional power encoding
# the script seems to get stuck on 1s and 50s which means i probably
#  have an off-by-one bug somewhere

import random
from utils import hdv, bind, bundle, cossim, make_bins


# make codebooks for 3 variables: x, y, z
# each codebook represents a contiguous vector field
codebook_size = 100
x_codebook = make_bins(bins=codebook_size, n=10_000)
y_codebook = make_bins(bins=codebook_size, n=10_000)
z_codebook = make_bins(bins=codebook_size, n=10_000)

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

# create superimposed estimate vectors for 2 of the 3 operand HVs
x_est_hv = bundle(*x_codebook)
y_est_hv = bundle(*y_codebook)
z_est_hv = bundle(*z_codebook)

def find_best_est(codebook, est, param2, param3, bound_hv):
  most_sim = cossim(est, bound_hv)
  for idx in range(1, len(codebook)):
    hv = codebook[idx]
    est = bind(bound_hv, param2, param3)
    sim = cossim(hv, est)
    if sim > most_sim:
      most_sim_idx = idx
      most_sim = sim
  return (most_sim_idx, codebook[most_sim_idx])


print()

# find x
(x_most_sim_idx, x_est_hv) = find_best_est(
  x_codebook,
  x_est_hv, y_est_hv, z_est_hv,
  bound_hv
)

# find y
(y_most_sim_idx, y_est_hv) = find_best_est(
  y_codebook,
  y_est_hv, x_est_hv, z_est_hv,
  bound_hv
)

# find z
(z_most_sim_idx, z_est_hv) = find_best_est(
  z_codebook,
  z_est_hv, x_est_hv, y_est_hv,
  bound_hv
)

# shift to account for index starting at 1 instead of 0
x_most_sim_idx += 1
y_most_sim_idx += 1
z_most_sim_idx += 1

# the big reveal
print()
print(f'\t\tx * y * z = S')
print(f'selected\t{x_idx} * {y_idx} * {z_idx} = {x_idx*y_idx*z_idx}')
print(f'inferred\t{x_most_sim_idx} * {y_most_sim_idx} * {z_most_sim_idx} = {x_most_sim_idx*y_most_sim_idx*z_most_sim_idx}')

print('cossim(x_hv, x_est_hv)', cossim(x_hv, x_est_hv))
print('cossim(y_hv, y_est_hv)', cossim(y_hv, y_est_hv))
print('cossim(z_hv, z_est_hv)', cossim(z_hv, z_est_hv))

est_bound_hv = bind(x_est_hv, y_est_hv, z_est_hv)
print('bound_hv', cossim(bound_hv, est_bound_hv))
