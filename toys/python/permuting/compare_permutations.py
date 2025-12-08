# Partial permutation using pair-wise rotation
#  of randomly selected hypervector elements.

import numpy as np
from numpy.linalg import norm
import random
import copy

from utils import sim, permute, hv
from utils import partial_random_pairs_permute
from utils import partial_ordered_pairs_permute


dims = 10000

hv = hv(n=dims)
hv_permuted1 = permute(hv)
print('Cyclic shift towards tail by 1 position')
print('orig', hv)
print('shifted 1' , hv_permuted1)
print('sim', sim(hv, hv_permuted1))
print()

print('swap 100% of the elements - ordered')
hv_1, swaps = partial_ordered_pairs_permute(hv, 1.00)
print(hv_1, len(swaps)*2)
print('sim', sim(hv, hv_1))
print()
print('swap 100% of the elements - randomly')
hv_1, swaps = partial_random_pairs_permute(hv, 1.00)
print(hv_1, len(swaps)*2)
print('sim', sim(hv, hv_1))
print()

print('swap 75% of the elements - ordered')
hv_75, swaps = partial_ordered_pairs_permute(hv, 0.75)
print(hv_75, len(swaps)*2)
print('sim', sim(hv, hv_75))
print()
print('swap 75% of the elements - randomly')
hv_75, swaps = partial_random_pairs_permute(hv, 0.75)
print(hv_75, len(swaps)*2)
print('sim', sim(hv, hv_75))
print()

print('swap 50% of the elements - ordered')
hv_50, swaps = partial_ordered_pairs_permute(hv, 0.50)
print(hv_50, len(swaps)*2)
print('sim', sim(hv, hv_50))
print()
print('swap 50% of the elements - randomly')
hv_50, swaps = partial_random_pairs_permute(hv, 0.50)
print(hv_50, len(swaps)*2)
print('sim', sim(hv, hv_50))
print()

print('swap 25% of the elements - ordered')
hv_25, swaps = partial_ordered_pairs_permute(hv, 0.25)
print(hv_25, len(swaps)*2)
print('sim', sim(hv, hv_25))
print()
print('swap 25% of the elements - randomly')
hv_25, swaps = partial_random_pairs_permute(hv, 0.25)
print(hv_25, len(swaps)*2)
print('sim', sim(hv, hv_25))
print()

print('swap 0% of the elements - ordered')
hv_0, swaps = partial_ordered_pairs_permute(hv, 0.00)
print(hv_0, len(swaps)*2)
print('sim', sim(hv, hv_0))
print()
print('swap 0% of the elements - randomly')
hv_0, swaps = partial_random_pairs_permute(hv, 0.00)
print(hv_0, len(swaps)*2)
print('sim', sim(hv, hv_0))
print()
