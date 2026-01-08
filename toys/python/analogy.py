# Analogies only work when unbind is exact


import numpy as np
from numpy.linalg import norm

from utils import *

# keys of the maps
country = hdv()
capital = hdv()
currency = hdv()

# country values
usa = hdv()
mex = hdv()
hun = hdv()

# capital values
wdc = hdv()
mxc = hdv()
bud = hdv()

# currency values
usd = hdv()
mxn = hdv()
huf = hdv()

# country maps
usa_map = bundle(bind(country, usa), bind(capital, wdc), bind(currency, usd))
mex_map = bundle(bind(country, mex), bind(capital, mxc), bind(currency, mxn))
hun_map = bundle(bind(country, hun), bind(capital, bud), bind(currency, huf))

print(f'united states map vector {usa_map[0:3]}...{usa_map[-3:]}')
print(f'mexico map vector {mex_map[0:3]}...{mex_map[-3:]}')
print(f'hungary map vector {hun_map[0:3]}...{hun_map[-3:]}')
print()

# this analogy represents a table of all countries and their mapped values
analogy = bind(hun_map, usa_map, mex_map)

# we can query the analogy by removing things from it
query = unbind(analogy, hun_map, usd)
print("what is the dollar of mexico?")
print(f'how similar is the query to USD?\t{cossim(query, usd)}')
print(f'how similar is the query to MXN?\t{cossim(query, mxn)}')
print(f'how similar is the query to HUF?\t{cossim(query, huf)}')
print()
print()

# we can query the analogy is different ways
query = unbind(analogy, usa_map, mxc)
print("what is the mexico city of hungary?")
print(f'how similar is the query to Washington DC?\t{cossim(query, wdc)}')
print(f'how similar is the query to Mexico City?  \t{cossim(query, mxc)}')
print(f'how similar is the query to Budapest?     \t{cossim(query, bud)}')
print(f'how similar is the query to USD?\t{cossim(query, usd)}')
print(f'how similar is the query to MXN?\t{cossim(query, mxn)}')
print(f'how similar is the query to HUF?\t{cossim(query, huf)}')
print(f'how similar is the query to United States?\t{cossim(query, usa)}')
print(f'how similar is the query to Mexico?       \t{cossim(query, mex)}')
print(f'how similar is the query to Hungary?      \t{cossim(query, hun)}')
print()
print()
