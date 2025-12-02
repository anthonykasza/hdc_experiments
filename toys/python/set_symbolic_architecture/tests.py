from utils import *

# The maximum number of elements a set can contain.
#  this value also influences the largest possible
#  value of any element.
dims = 1000
dims = 10

print('Test symbol generation and id')
symbol1 = symbol(dims=dims, id=1)
symbol2 = symbol(dims=dims, id=2)
symbol3 = symbol(dims=dims, id=3)

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


print('Test similarity')
print(f'symbol1 to bundle sim:, {sim(symbol1, bundle_1_2)}')
print(f'symbol2 to bundle sim:, {sim(symbol2, bundle_1_2)}')
print(f'symbol3 to bundle sim:, {sim(symbol3, bundle_1_2)}')
print()


print('Test subtract')
recovered1 = subtract(bundle_1_2, id=2, dims=dims)
print(f'The recovered set, {recovered1}\n  of size {len(recovered1)}')
for element in recovered1:
  id = element % dims
  print(f'value: {element}, id: {id}')
print()


print(f'Test bind')
binding_1_2 = bind(symbol1, symbol2)
print(f'The binding of ones and twos, {binding_1_2}\n  of size {len(binding_1_2)}')
for element in binding_1_2:
  print(f'value: {element}, id: {element % len(binding_1_2)}')
print()

print('Test similarity - binding')
print(f'symbol1 to binding sim:, {sim(symbol1, binding_1_2)}')
print(f'symbol2 to binding sim:, {sim(symbol2, binding_1_2)}')
print(f'symbol3 to binding sim:, {sim(symbol3, binding_1_2)}')
print()


print(f'Test unbind')
recovered1 = unbind(binding_1_2, id=1, dims=dims)
print(f'The recovered symbol1 {recovered1}\n  of size {len(recovered1)}')
for element in recovered1:
  print(f'value: {element}, id: {element % dims}')
print()

print('Test similarity - unbinding')
print(f'symbol1 to recovered1 sim:, {sim(symbol1, recovered1)}')
print(f'symbol2 to recovered1 sim:, {sim(symbol2, recovered1)}')
print(f'binding to recovered1 sim:, {sim(binding_1_2, recovered1)}')
print()
