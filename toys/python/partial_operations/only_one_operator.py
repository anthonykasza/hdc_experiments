# Binding and bundling operations are interchangeable
#  and only interfere if permutations are used.
#
# Without permuting indices this is essentially
#  the same as using one hv for bundling and one hv
#  for binding.


import copy
import numpy as np
from numpy.linalg import norm

def permute(hv, positions=1):
  return np.roll(hd, positions, axis=0)


def inverse(hv):
  return np.array([1 / x if x != 0 else 0 for x in hv])


def operator(*hvs, mode="bundle"):
  """
     No clipping or normalization, unbounded growth

     Bundle: adds even indices and multiplies odd indices
     Bind:   multiplies even indices and adds odd indices

     Unbundle: undoes bundle
     Unbind:   undoes bind
  """
  if len(hvs) < 2:
    raise ValueError("Provide at least one array-like input")
  hvs = [np.asarray(hv) for hv in hvs]

  if mode == "bundle":
    result = np.zeros_like(hvs[0], dtype=float)
    summed = np.sum(hvs, axis=0)
    prod = np.prod(hvs, axis=0)
    result[::2] = summed[::2]   # add even indices
    result[1::2] = prod[1::2]   # multipy odd indices

  elif mode == "bind":
    result = np.zeros_like(hvs[0], dtype=float)
    summed = np.sum(hvs, axis=0)
    prod = np.prod(hvs, axis=0)
    result[::2] = prod[::2]     # multiply even indices
    result[1::2] = summed[1::2] # add odd indices

  elif mode == "unbind":
    result = copy.copy(hvs[0])
    for hv in hvs[1:]:
      result[::2] = result[::2] * inverse(hv)[::2] # divide even indices
      result[1::2] = result[1::2] - hv[1::2]       # subtract odd indices

  elif mode == "unbundle":
    result = copy.copy(hvs[0])
    for hv in hvs[1:]:
      result[::2] = result[::2] - hv[::2]             # subtract even indices
      result[1::2] = result[1::2] * inverse(hv)[1::2] # divide odd indices

  else:
    raise ValueError("mode must be '(un)bundle' or '(un)bind'")

  return result


def bind(*hvs):
  return operator(*hvs, mode="bind")

def bundle(*hvs):
  return operator(*hvs, mode="bundle")

def unbind(*hvs):
  return operator(*hvs, mode="unbind")

def unbundle(*hvs):
  return operator(*hvs, mode="unbundle")

def new_symbol(n):
  return np.random.choice([1,-1], size=n)

def sim(new_symbol1, new_symbol2):
  """Similarity -1 to 1"""
  if norm(new_symbol1) == 0 or norm(new_symbol2) == 0:
    return 0
  return np.dot(new_symbol1, new_symbol2) / (norm(new_symbol1) * norm(new_symbol2))




# half will be for binding, half for bundling
dims = 14000

# keys of the maps
country = new_symbol(dims)
capital = new_symbol(dims)
currency = new_symbol(dims)

# country values
usa = new_symbol(dims)
mex = new_symbol(dims)
hun = new_symbol(dims)

# capital values
wdc = new_symbol(dims)
mxc = new_symbol(dims)
bud = new_symbol(dims)

# currency values
usd = new_symbol(dims)
mxn = new_symbol(dims)
huf = new_symbol(dims)





print("ANALOGY binding of bundles of bindings")

# country maps
usa_map = bundle(bind(country, usa), bind(capital, wdc), bind(currency, usd))
mex_map = bundle(bind(country, mex), bind(capital, mxc), bind(currency, mxn))
hun_map = bundle(bind(country, hun), bind(capital, bud), bind(currency, huf))

# this analogy represents a table of all countries and their mapped values
analogy = bind(hun_map, usa_map, mex_map)

# we can query the analogy by removing things from it
query = unbind(unbind(analogy, hun_map), usd)
print("what is the dollar of mexico?")
print(f'sim with USD\t{sim(query, usd)}')
print(f'sim with MXN\t{sim(query, mxn)}')
print(f'sim with HUF\t{sim(query, huf)}')
print()

# we can query the analogy is different ways
query = unbind(unbind(analogy, usa_map), mxc)
print("what is the mexico city of hungary?")
print(f'sim with Washington DC\t{sim(query, wdc)}')
print(f'sim with Mexico City\t{sim(query, mxc)}')
print(f'sim with Budapest\t{sim(query, bud)}')
print()
print()



print("ANALOGY bundle of bindings of bundles")

# country maps
usa_map = bind(bundle(country, usa), bundle(capital, wdc), bundle(currency, usd))
mex_map = bind(bundle(country, mex), bundle(capital, mxc), bundle(currency, mxn))
hun_map = bind(bundle(country, hun), bundle(capital, bud), bundle(currency, huf))

# this analogy represents a table of all countries and their mapped values
analogy = bundle(hun_map, usa_map, mex_map)

# we can query the analogy by removing things from it
query = unbundle(unbundle(analogy, hun_map), usd)
print("what is the dollar of mexico?")
print(f'sim with USD\t{sim(query, usd)}')
print(f'sim with MXN\t{sim(query, mxn)}')
print(f'sim with HUF\t{sim(query, huf)}')
print()

# we can query the analogy is different ways
query = unbundle(unbundle(analogy, usa_map), mxc)
print("what is the mexico city of hungary?")
print(f'sim with Washington DC\t{sim(query, wdc)}')
print(f'sim with Mexico City\t{sim(query, mxc)}')
print(f'sim with Budapest\t{sim(query, bud)}')
print()
