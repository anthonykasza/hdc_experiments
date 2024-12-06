
from bsbc_utils import hdv, bundle, bind, permute
from bsbc_utils import cossim, inverse, decompress
from bsbc_utils import flatten, make_levels

from bsbc_utils import sim_cyclic, bundle_cyclic


# Test generation, decompression, flatten, cossim
block_count = 4
block_size = 4
dims = block_count * block_size

hv1, hv1_compressed = hdv(dims, block_count)
print(f'A new random hypervector')
print(f'{hv1}')
print()
print(f'The hv compressed to only the "on" elements')
print(f'{hv1_compressed}')
print()

hv1_c_decompressed = decompress(hv1_compressed, dims, block_count)
print(f'The original hv expanded from the compressed representation')
print(f'{hv1_c_decompressed}')
print()

hv1_c_d_f = flatten(hv1_c_decompressed)
print(f'The decompressed hv flattened without the blocks')
print(f'{hv1_c_d_f}')
print()

sim = cossim(hv1_c_decompressed, hv1)
print(f'The similarity between the original hv and the decompressed hv')
print(f'{sim}')
print()
print()

# Test inverse, permute
print(f'The compressed hv')
print(f'{hv1_compressed}')
print()
print(f'The inversion of the compressed hv (block size minus value)')
print(f'{inverse(hv1_compressed, block_size=block_size)}')
print()

print(f'The compressed hv')
print(f'{hv1_compressed}')
print()
print(f'Block permutation of the compressed hv (1 to the right)')
print(f'{permute(hv1_compressed)}')
print()

print(f'The expanded hv')
print(f'{hv1_c_decompressed}')
print()
print(f'Block permutation of the expanded hv (1 to the right)')
print(f'{permute(hv1_c_decompressed)}')
print()
print()

# Test bundle
block_count = 8
block_size = 64
dims = block_count * block_size
hv1, hv1_c = hdv(dims, block_count)
hv2, hv2_c = hdv(dims, block_count)
hv3, hv3_c = hdv(dims, block_count)
hv4, hv4_c = hdv(dims, block_count)
hv5, hv5_c = hdv(dims, block_count)
noise, noise_c = hdv(dims, block_count)
bundle_c = bundle(hv1_c, hv2_c, hv3_c, hv4_c, hv5_c)

print(f'Compressed hvs and their bundle')
print(f'hv1_c:    {hv1_c}')
print(f'hv2_c:    {hv2_c}')
print(f'hv3_c:    {hv3_c}')
print(f'hv4_c:    {hv4_c}')
print(f'hv5_c:    {hv5_c}')
print(f'bundle_c: {bundle_c}')
print()

b = decompress(bundle_c, dims, block_count)
print(f'hv1 to decompressed bundle: {cossim(hv1, b)}')
print(f'hv2 to decompressed bundle: {cossim(hv2, b)}')
print(f'hv3 to decompressed bundle: {cossim(hv3, b)}')
print(f'hv4 to decompressed bundle: {cossim(hv4, b)}')
print(f'hv5 to decompressed bundle: {cossim(hv5, b)}')
print(f'noise to decompressed bundle: {cossim(noise, b)}')
print()

# Test leveling
block_count = 8
block_size = 64
dims = block_count * block_size
hv1, hv1_c = hdv(dims, block_count)
hv2, hv2_c = hdv(dims, block_count)
levels_c = make_levels(hv1_c, hv2_c, block_size=block_size)
print('Leveling between hv')
print(f'hv1_c:  {hv1_c}')
print(f'hv2_c:  {hv2_c}')
print()

for idx in range(len(levels_c)):
  level_c = levels_c[idx]
  level_d = decompress(level_c, dims, block_count)
  if idx == 0:
    print(idx, level_c)
    continue
  level_prev_c = levels_c[idx-1]
  level_prev_d = decompress(level_prev_c, dims, block_count)
  print(idx, level_c, cossim(level_d, level_prev_d))


level_first_c = levels_c[0]
level_mid_c = levels_c[len(levels_c)//2]
level_last_c = levels_c[-1]
level_first_d = decompress(level_first_c, dims, block_count)
level_mid_d = decompress(level_mid_c, dims, block_count)
level_last_d = decompress(level_last_c, dims, block_count)
print(f'level0 to last level{len(levels_c)} sim: {cossim(level_first_d, level_last_d)}')
print(f'level0 to middle level{len(levels_c)//2} sim: {cossim(level_first_d, level_mid_d)}')
print(f'middle level{len(levels_c)//2} to last level{len(levels_c)} sim: {cossim(level_first_d, level_mid_d)}')
print()
print()

# Test bind
block_count = 128
block_size = 64
dims = block_size * block_count
hv1, hv1_c = hdv(dims, block_count)
hv2, hv2_c = hdv(dims, block_count)
hv3, hv3_c = hdv(dims, block_count)
hv4, hv4_c = hdv(dims, block_count)
hv5, hv5_c = hdv(dims, block_count)
noise, noise_c = hdv(dims, block_count)
binding_c = bind(hv1_c, hv2_c, hv3_c, hv4_c, hv5_c, block_size=block_size)

print(f'Binding produces an hv which is dissimilar to all inputs')
print(f'hv1_c:     {hv1_c}')
print(f'hv2_c:     {hv2_c}')
print(f'hv3_c:     {hv3_c}')
print(f'hv4_c:     {hv4_c}')
print(f'hv5_c:     {hv5_c}')
print(f'binding_c: {binding_c}')
print()

binding = decompress(binding_c, dims, block_count)
print(f'hv1 to decompressed binding: {cossim(hv1, binding)}')
print(f'hv2 to decompressed binding: {cossim(hv2, binding)}')
print(f'hv3 to decompressed binding: {cossim(hv3, binding)}')
print(f'hv4 to decompressed binding: {cossim(hv4, binding)}')
print(f'hv5 to decompressed binding: {cossim(hv5, binding)}')
print(f'noise to decompressed binding: {cossim(noise, binding)}')
print()

hv1_c_inverse = inverse(hv1_c, block_size=block_size)
query_c = bind(binding_c, hv1_c_inverse, block_size=block_size)
query_d = decompress(query_c, dims, block_count)
print('Querying the binding does not seem to work as expected')
print(f'query to hv1: {cossim(hv1, query_d)}')
print(f'query to hv2: {cossim(hv2, query_d)}')
print(f'query to hv3: {cossim(hv3, query_d)}')
print(f'query to hv4: {cossim(hv4, query_d)}')
print(f'query to hv5: {cossim(hv5, query_d)}')
print(f'query to noise: {cossim(noise, query_d)}')
print()


# Test cyclic similarity
print('Test cyclic group similarity')
block_size_1 = 2      # binary just like BSC
block_size_2 = 360    # a cyclic group of size 360
hv1 = [0,   1,   1,   1,   1,   0]
hv2 = [360, 180, 180, 180, 180, 360]
similarity = sim_cyclic(hv1, hv2, block_size_1, block_size_2)
print(f"{block_size_1} {block_size_2} {similarity}")

block_size_1 = 4
block_size_2 = 360
hv1 = [1,  3,   3,   3,   3,   2]
hv2 = [90, 270, 270, 270, 270, 180]
similarity = sim_cyclic(hv1, hv2, block_size_1, block_size_2)
print(f"{block_size_1} {block_size_2} {similarity}")

block_size_1 = 64
block_size_2 = 128
hv1 = [0, 64,  54,  12, 32, 32, 32, 10]
hv2 = [0, 128, 108, 24, 64, 64, 64, 20]
similarity = sim_cyclic(hv1, hv2, block_size_1, block_size_2)
print(f"{block_size_1} {block_size_2} {similarity}")

block_size_1 = 64
block_size_2 = 64
hv1 = [0, 64, 54, 12, 32, 32, 32, 10]
hv2 = [1, 63, 55, 11, 33, 31, 33, 9]
similarity = sim_cyclic(hv1, hv2, block_size_1, block_size_2)
print(f"{block_size_1} {block_size_2} {similarity}")
print()


# Test bundle_cyclic
block_count = 5
block_size = 360
dims = block_count * block_size
hv1, hv1_c = hdv(dims, block_count)
hv2, hv2_c = hdv(dims, block_count)
hv3, hv3_c = hdv(dims, block_count)
hv4, hv4_c = hdv(dims, block_count)
hv5, hv5_c = hdv(dims, block_count)
noise, noise_c = hdv(dims, block_count)
bundle_c_cyc = bundle_cyclic(hv1_c, hv2_c, hv3_c, hv4_c, hv5_c)

print(hv1_c)
print(hv2_c)
print(hv3_c)
print(hv4_c)
print(hv5_c)
print(bundle_c_cyc)
print()

h1 = [0,   0,   0,   0]
h2 = [90,  90,  90,  90]
h3 = [180, 180, 180, 180]
h4 = [270, 270, 270, 270]
b = bundle_cyclic(h1, h2, h3, h4, block_size=360)
print(h1)
print(h2)
print(h3)
print(h4)
print(b)
