import numpy as np

#np.random.seed(42)
D = 10000

def ternary_map_hv(D):
  return np.random.randint(-1, 2, D).astype(float)

def hlb_hv(D):
  n1 = np.random.normal(-1, 1/np.sqrt(D), D)
  n2 = np.random.normal(1, 1/np.sqrt(D), D)
  mask = np.random.rand(D) > 0.5
  return np.where(mask, n1, n2)

def scaled_cosine(a, b):
  return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

hv1 = ternary_map_hv(D)
hv2 = ternary_map_hv(D)
hv3 = ternary_map_hv(D)
hv4 = ternary_map_hv(D)
noise = ternary_map_hv(D)

hv1_hlb = hlb_hv(D)
hv2_hlb = hlb_hv(D)
hv3_hlb = hlb_hv(D)
hv4_hlb = hlb_hv(D)
noise_hlb = hlb_hv(D)

bundle_map = hv1 + hv2 + hv3 + hv4
bundle_hlb = hv1_hlb + hv2_hlb + hv3_hlb + hv4_hlb

print("=== Bundling Similarity (MAP) ===")
for i, hv in enumerate([hv1, hv2, hv3, hv4, noise], start=1):
  sim = scaled_cosine(hv, bundle_map)
  if i == 5:
    print(f"NOISE vs bundle: {sim:.3f}")
  else:
    print(f"HV{i} vs bundle: {sim:.3f}")

print("\n=== Bundling Similarity (HLB) ===")
for i, hv in enumerate([hv1_hlb, hv2_hlb, hv3_hlb, hv4_hlb, noise_hlb], start=1):
  sim = scaled_cosine(hv, bundle_hlb)
  if i == 5:
    print(f"NOISE vs bundle: {sim:.3f}")
  else:
    print(f"HV{i} vs bundle: {sim:.3f}")



bound_map = hv1 * hv2
bound_hlb = hv1_hlb * hv2_hlb

print("\n=== Binding Similarity ===")
sim_map1 = scaled_cosine(hv1, bound_map)
sim_map2 = scaled_cosine(hv2, bound_map)
sim_map_noise = scaled_cosine(noise, bound_map)
sim_hlb1 = scaled_cosine(hv1_hlb, bound_hlb)
sim_hlb2 = scaled_cosine(hv2_hlb, bound_hlb)
sim_hlb_noise = scaled_cosine(noise_hlb, bound_hlb)

print(f"MAP HV1 vs bound: {sim_map1:.3f}")
print(f"MAP HV2 vs bound: {sim_map2:.3f}")
print(f"MAP NOISE vs bound: {sim_map_noise:.3f}")
print(f"HLB HV1 vs bound: {sim_hlb1:.3f}")
print(f"HLB HV2 vs bound: {sim_hlb2:.3f}")
print(f"HLB NOISE vs bound: {sim_hlb_noise:.3f}")

recovered_hv1 = bound_map * hv2
recovered_hv2 = bound_map * hv1
recovered_hv1_hlb = bound_hlb * hv2_hlb
recovered_hv2_hlb = bound_hlb * hv1_hlb

print("\n=== Unbinding Recovery Similarity ===")
sim_rec1 = scaled_cosine(hv1, recovered_hv1)
sim_rec2 = scaled_cosine(hv2, recovered_hv2)
sim_rec1_hlb = scaled_cosine(hv1_hlb, recovered_hv1_hlb)
sim_rec2_hlb = scaled_cosine(hv2_hlb, recovered_hv2_hlb)

print(f"MAP recovered HV1 vs original: {sim_rec1:.3f}")
print(f"MAP recovered HV2 vs original: {sim_rec2:.3f}")
print(f"HLB recovered HV1 vs original: {sim_rec1_hlb:.3f}")
print(f"HLB recovered HV2 vs original: {sim_rec2_hlb:.3f}")
