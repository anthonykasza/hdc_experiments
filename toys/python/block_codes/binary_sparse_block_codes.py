import random

# return a binary sparse block code hypervector
def hdv_bsbc(dimensions=10_000, number_of_blocks=1000):
  h = []
  block_size = dimensions // number_of_blocks
  on_bit_indices = []
  for block in range(number_of_blocks):
    on_bit = random.randint(0, block_size-1)
    on_bit_indices.append(on_bit)
    # all element in the block are zero ...
    tmp = [0] * block_size
    # ... except a a randomly chosen index is set to 1
    tmp[on_bit] = 1
    h.append(tmp)
  return h, on_bit_indices


# given a list of the indices of the 'on' bits
#  and the original dims, reconstrcut the BSBC hypervector
def decompress(onbits, dimensions, number_of_blocks):
  h = []
  block_size = dimensions // number_of_blocks
  for block in range(number_of_blocks):
    on_bit = onbits[block]
    tmp = [0] * block_size
    tmp[on_bit] = 1
    h.append(tmp)
  return h


#dimensions = 1200
#number_of_blocks = 40
dimensions = 12
number_of_blocks = 4

h, on_bit_indices = hdv_bsbc(dimensions, number_of_blocks)
reconstructed = decompress(on_bit_indices, dimensions, number_of_blocks)

print("the full hypervector, block segments shown")
print(h)
print()
print("just the 'on' bits of the hypervector (compressed BSBC)")
print(on_bit_indices)
print()
print("lossless decompression")
print(reconstructed)
