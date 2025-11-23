from utils import *

# The maximum number of elements a set can contain.
#  this value also influences the largest possible
#  value of any element.
dims = 1000
dims = 10

print('Test symbol generation and id')
symbol1 = new(dims=dims, id=1)
symbol2 = new(dims=dims, id=2)
symbol3 = new(dims=dims, id=3)

print(f'The symbol with id 1, {symbol1}')
for element in symbol1:
  id = element % dims
  print(f'value: {element}, id: {id}')

print(f'The symbol with id 2, {symbol2}')
for element in symbol2:
  id = element % dims
  print(f'value: {element}, id: {id}')

print(f'The symbol with id 3, {symbol3}')
for element in symbol3:
  id = element % dims
  print(f'value: {element}, id: {id}')

print()


print('Test bundle')
bundle_1_2 = bundle(symbol1, symbol2)
print(f'The bundle of ones and twos, {bundle_1_2}\n  of size {len(bundle_1_2)}')
for element in bundle_1_2:
  id = element % dims
  print(f'value: {element}, id: {id}')
print()


print('Test similarity - bundle is indeed similar to constituents')
print(f'symbol1 to bundle sim:, {sim(symbol1, bundle_1_2)}')
print(f'symbol2 to bundle sim:, {sim(symbol2, bundle_1_2)}')
print(f'symbol3 to bundle sim:, {sim(symbol3, bundle_1_2)}')
print()


print('Test subtract - the set size is cut in half')
recovered_ones = subtract(bundle_1_2, id=2)
print(f'The recovered set, {recovered_ones}\n  of size {len(recovered_ones)}')
for element in recovered_ones:
  id = element % dims
  print(f'value: {element}, id: {id}')
print()


print(f'Test bind')
binding_1_2 = bind(symbol1, symbol2)
print(f'The binding of ones and twos, {bundle_1_2}\n  of size {len(bundle_1_2)}')
for element in binding_1_2:
  print(f'value: {element}, id: {element % len(binding_1_2)}')
print()

print('Test similarity - binding')
print(f'symbol1 to binding sim:, {sim(symbol1, binding_1_2)}')
print(f'symbol2 to binding sim:, {sim(symbol2, binding_1_2)}')
print()


print(f'Test unbind')
recovered_ones = unbind(binding_1_2, id=1)
print(f'The recovered symbol1 {recovered_ones}  of size {len(recovered_ones)}')
for element in recovered_ones:
  print(f'value: {element}, id: {element % len(recovered_ones)}')
print()

print('Test similarity - unbinding')
print(f'symbol1 to recovered_ones sim:, {sim(symbol1, recovered_ones)}')
print(f'symbol2 to recovered_ones sim:, {sim(symbol2, recovered_ones)}')
print(f'binding to recovered_ones sim:, {sim(binding_1_2, recovered_ones)}')
print()
