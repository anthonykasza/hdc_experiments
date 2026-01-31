# Inspired by tropical algebra

import numpy as np
from numpy.linalg import norm


def new_hv(dims=10000, low=-1, high=1, fill=None):
  if fill is not None:
    return np.array([fill] * dims)
  choices = np.arange(low, high + 1)
  choices = choices[choices != 0]
  return np.random.choice(choices, size=dims)

def bind(h1, h2):
  '''multiplication is addition'''
  return h1 + h2

def unbind(h1, h2):
  return h1 - h2

def bundle(h1, h2, method='min'):
  '''addition is max or min'''
  if method == 'min':
    return np.array([min(h1[idx], h2[idx]) for idx in range(len(h1))])
  elif method == 'max':
    return np.array([max(h1[idx], h2[idx]) for idx in range(len(h1))])
  else:
    raise

def sim(hv1, hv2):
  hv1_norm = norm(hv1)
  hv2_norm = norm(hv2)
  if hv1_norm == 0 or hv2_norm == 0:
    return 0.0
  return np.dot(hv1, hv2) / (hv1_norm * hv2_norm)


# keys of the maps
country = new_hv()
capital = new_hv()
currency = new_hv()

# country values
usa = new_hv()
mex = new_hv()
hun = new_hv()

# capital values
wdc = new_hv()
mxc = new_hv()
bud = new_hv()

# currency values
usd = new_hv()
mxn = new_hv()
huf = new_hv()

# country maps
usa_map = bundle(bundle(bind(country, usa), bind(capital, wdc)), bind(currency, usd))
mex_map = bundle(bundle(bind(country, mex), bind(capital, mxc)), bind(currency, mxn))
hun_map = bundle(bundle(bind(country, hun), bind(capital, bud)), bind(currency, huf))

print(f'united states map vector {usa_map[0:3]}...{usa_map[-3:]}')
print(f'mexico map vector {mex_map[0:3]}...{mex_map[-3:]}')
print(f'hungary map vector {hun_map[0:3]}...{hun_map[-3:]}')
print()

# this analogy represents a table of all countries and their mapped values
analogy = bind(bind(hun_map, usa_map), mex_map)

# we can query the analogy by removing things from it
query = unbind(unbind(analogy, hun_map), usd)
print("what is the dollar of mexico?")
print(f'how similar is the query to USD?\t{sim(query, usd)}')
print(f'how similar is the query to MXN?\t{sim(query, mxn)}')
print(f'how similar is the query to HUF?\t{sim(query, huf)}')
print()
print()

# we can query the analogy is different ways
query = unbind(unbind(analogy, usa_map), mxc)
print("what is the mexico city of hungary?")
print(f'how similar is the query to Washington DC?\t{sim(query, wdc)}')
print(f'how similar is the query to Mexico City?  \t{sim(query, mxc)}')
print(f'how similar is the query to Budapest?     \t{sim(query, bud)}')
print(f'how similar is the query to USD?\t{sim(query, usd)}')
print(f'how similar is the query to MXN?\t{sim(query, mxn)}')
print(f'how similar is the query to HUF?\t{sim(query, huf)}')
print(f'how similar is the query to United States?\t{sim(query, usa)}')
print(f'how similar is the query to Mexico?       \t{sim(query, mex)}')
print(f'how similar is the query to Hungary?      \t{sim(query, hun)}')
print()
print()
