import numpy as np

from clipping_strategies import new_hv
from clipping_strategies import clip_sign
from clipping_strategies import CountingBundle, ThresholdBundle
from clipping_strategies import BatchBundle, ExplicitBundle

# The signals do not change, but the clipping strategies do
signals = [new_hv(n=5) for x in range(10)]


print('Counting constituents')
cb = CountingBundle(rate=3, clip_func=clip_sign, n=5)
for idx in range(len(signals)):
  s = signals[idx]
  print(f'{idx} current:\t{cb.value}')
  print(f'{idx} adding in:\t{s}')
  cb.bundle(s)
print(f'final values:\t{cb.value}')
print()
print()

print('Thresholding elements')
tb = ThresholdBundle(thresh=5, clip_func=clip_sign, n=5)
for idx in range(len(signals)):
  s = signals[idx]
  print(f'{idx} current:\t{tb.value}')
  print(f'{idx} adding in:\t{s}')
  tb.bundle(s)
print(f'final values:\t{tb.value}')
print()
print()

print('After each call to bundle()')
bb = BatchBundle(clip_func=clip_sign, n=5)
for idx in range(len(signals)):
  s = signals[idx]
  print(f'{idx} current:\t{bb.value}')
  print(f'{idx} adding in:\t{s}')
  bb.bundle(s)
print(f'final values:\t{bb.value}')
print()
print()

