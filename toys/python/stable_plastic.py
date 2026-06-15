# Stability vs plasticity
# Shifting the entire codebook in a structured way appears
#  to preserve the analogy

import numpy as np
from numpy.linalg import norm

from utils import *


def representation_shift(codebook, elements=5):
  '''All symbols in the codebook have some randomly selected elements shifted'''
  new_codebook = {}
  for concept_name, hv in codebook.items():
    shifted_symbol = hv.copy()

    unchanged = list(range(len(hv)))

    # Cyclic shift elements around their range
    while elements > 0:
      idx = np.random.choice(unchanged)
      # 1s become 0
      if shifted_symbol[idx] == 1:
        shifted_symbol[idx] = 0
      # 0s become -1
      elif shifted_symbol[idx] == 0:
        shifted_symbol[idx] = -1
      # -1s become 1
      elif shifted_symbol[idx] == -1:
        shifted_symbol[idx] = 1

      unchanged.remove(idx)
      elements -= 1

    new_codebook[concept_name] = shifted_symbol
  return new_codebook


def cleanup(query_hv, codebook):
  best_concept = ''
  best_sim = 0.0

  for concept_name, hv in codebook.items():
    this_sim = cossim(query_hv, hv)
    if this_sim > best_sim:
      best_concept = concept_name
      best_sim = this_sim

  return best_concept, best_sim


codebook = {}

# keys of the maps
codebook['country'] = hdv()
codebook['capital'] = hdv()
codebook['currency'] = hdv()

# country values
codebook['usa'] = hdv()
codebook['mex'] = hdv()
codebook['hun'] = hdv()

# capital values
codebook['wdc'] = hdv()
codebook['mxc'] = hdv()
codebook['bud'] = hdv()

# currency values
codebook['usd'] = hdv()
codebook['mxn'] = hdv()
codebook['huf'] = hdv()

# country maps
codebook['usa_map'] = bundle(bind(codebook['country'], codebook['usa']), bind(codebook['capital'], codebook['wdc']), bind(codebook['currency'], codebook['usd']))
codebook['mex_map'] = bundle(bind(codebook['country'], codebook['mex']), bind(codebook['capital'], codebook['mxc']), bind(codebook['currency'], codebook['mxn']))
codebook['hun_map'] = bundle(bind(codebook['country'], codebook['hun']), bind(codebook['capital'], codebook['bud']), bind(codebook['currency'], codebook['huf']))


# this analogy represents a table of all countries and their mapped values
analogy = bind(codebook['hun_map'], codebook['usa_map'], codebook['mex_map'])


# shift all representations in the codebook in a structured way
shift_percent = 0.25
shift_percent = 0.33
shift_percent = 0.66
shift_percent = 0.95
dims = len(analogy)
codebook = representation_shift(codebook, elements=dims * shift_percent)


# we can query the analogy by removing things from it
query = unbind(analogy, codebook['hun_map'], codebook['usd'])
print("what is the dollar of mexico?")
print(f'{cleanup(query, codebook)}')
print()

# we can query the analogy is different ways
query = unbind(analogy, codebook['usa_map'], codebook['mxc'])
print("what is the mexico city of hungary?")
print(f'{cleanup(query, codebook)}')
print()
