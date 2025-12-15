
import numpy as np
from numpy.linalg import norm

from utils import new_symbol, inverse, bundle, sim


def bind(*args):
  '''Element-wise addition on odd indices'''
  summed = np.sum(args, axis=0)
  result = np.zeros_like(summed)
  result[1::2] = summed[1::2]
  return result


dims = 2_000
signal1 = new_symbol(dims)
signal2 = new_symbol(dims)
signal3 = new_symbol(dims)
signal4 = new_symbol(dims)
noise = new_symbol(dims)

bundling_result = bundle(signal1, signal2, signal3, signal4)
binding_result = bind(signal1, signal2, signal3, signal4)

print(f'bundling_result to binding_result: {sim(bundling_result, binding_result)}')
print(f'signal1 to signal2: {sim(signal1, signal2)}')
print(f'signal1 to signal3: {sim(signal1, signal3)}')
print(f'signal1 to signal4: {sim(signal1, signal4)}')
print(f'signal1 to noise: {sim(signal1, noise)}')
print()
print(f'bundling_result to signal1: {sim(bundling_result, signal1)}')
print(f'bundling_result to signal2: {sim(bundling_result, signal2)}')
print(f'bundling_result to signal3: {sim(bundling_result, signal3)}')
print(f'bundling_result to signal4: {sim(bundling_result, signal4)}')
print(f'bundling_result to noise: {sim(bundling_result, noise)}')
print()
print(f'binding_result to signal1: {sim(binding_result, signal1)}')
print(f'binding_result to signal2: {sim(binding_result, signal2)}')
print(f'binding_result to signal3: {sim(binding_result, signal3)}')
print(f'binding_result to signal4: {sim(binding_result, signal4)}')
print(f'binding_result to noise: {sim(binding_result, noise)}')
print()
query_signal1 = bind(binding_result, signal2, signal3, signal4)
query_signal2 = bind(binding_result, signal1, signal3, signal4)
query_signal3 = bind(binding_result, signal1, signal2, signal4)
query_signal4 = bind(binding_result, signal1, signal2, signal3)
print(f'signal1 to recovered signal1: {sim(signal1, query_signal1)}')
print(f'signal2 to recovered signal2: {sim(signal2, query_signal2)}')
print(f'signal3 to recovered signal3: {sim(signal3, query_signal3)}')
print(f'signal4 to recovered signal4: {sim(signal4, query_signal4)}')
print()
