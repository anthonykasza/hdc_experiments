# Compare randomly initialized hv with low discrepency hv

import numpy as np

import sys
sys.path.insert(0, '../../')
from utils import hdv_ld, hdv

# low discrepency sobol default thresh
hv1 = hdv_ld(n=2**14)
print('ld 3/16', hv1, len(hv1), sum(hv1), np.mean(hv1), np.var(hv1))

# low discrepency sobol 0.5 thresh
hv2 = hdv_ld(n=2**14, thresh=0.5)
print('ld 0.5', hv2, len(hv2), sum(hv2), np.mean(hv2), np.var(hv2))

# numpy random choice
hv3 = hdv(n=2**14)
print('random', hv3, len(hv3), sum(hv3), np.mean(hv3), np.var(hv3))
