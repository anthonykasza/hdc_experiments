import numpy as np


def ternary_map_hv(D=10000):
  return np.random.randint(-1, 2, D).astype(float)

def hdv(D=10000):
  n1 = np.random.normal(-1, 1/np.sqrt(D), D)
  n2 = np.random.normal(1, 1/np.sqrt(D), D)
  mask = np.random.rand(D) > 0.5
  return np.where(mask, n1, n2)

def similarity(a, b):
  return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def bundle(*args):
  return np.sum(args, axis=0)

def bind(*args):
  return np.prod(args, axis=0)

def inverse(hv):
  return [1/x for x in hv]

def unbind(h1, h2):
  return bind(h1, inverse(h2))

if __name__ == '__main__':
  hv1 = ternary_map_hv()
  hv2 = ternary_map_hv()
  hv3 = ternary_map_hv()
  hv4 = ternary_map_hv()
  noise = ternary_map_hv()

  hv1_hlb = hdv()
  hv2_hlb = hdv()
  hv3_hlb = hdv()
  hv4_hlb = hdv()
  noise_hlb = hdv()

  bundle_map = hv1 + hv2 + hv3 + hv4
  bundle_hlb = hv1_hlb + hv2_hlb + hv3_hlb + hv4_hlb

  print("=== Bundling Similarity (MAP) ===")
  for i, hv in enumerate([hv1, hv2, hv3, hv4, noise], start=1):
    sim = similarity(hv, bundle_map)
    if i == 5:
      print(f"NOISE vs bundle: {sim:.3f}")
    else:
      print(f"HV{i} vs bundle: {sim:.3f}")

  print("\n=== Bundling Similarity (HLB) ===")
  for i, hv in enumerate([hv1_hlb, hv2_hlb, hv3_hlb, hv4_hlb, noise_hlb], start=1):
    sim = similarity(hv, bundle_hlb)
    if i == 5:
      print(f"NOISE vs bundle: {sim:.3f}")
    else:
      print(f"HV{i} vs bundle: {sim:.3f}")



  bound_map = hv1 * hv2
  bound_hlb = hv1_hlb * hv2_hlb

  print("\n=== Binding Similarity ===")
  sim_map1 = similarity(hv1, bound_map)
  sim_map2 = similarity(hv2, bound_map)
  sim_map_noise = similarity(noise, bound_map)
  sim_hlb1 = similarity(hv1_hlb, bound_hlb)
  sim_hlb2 = similarity(hv2_hlb, bound_hlb)
  sim_hlb_noise = similarity(noise_hlb, bound_hlb)

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
  sim_rec1 = similarity(hv1, recovered_hv1)
  sim_rec2 = similarity(hv2, recovered_hv2)
  sim_rec1_hlb = similarity(hv1_hlb, recovered_hv1_hlb)
  sim_rec2_hlb = similarity(hv2_hlb, recovered_hv2_hlb)

  print(f"MAP recovered HV1 vs original: {sim_rec1:.3f}")
  print(f"MAP recovered HV2 vs original: {sim_rec2:.3f}")
  print(f"HLB recovered HV1 vs original: {sim_rec1_hlb:.3f}")
  print(f"HLB recovered HV2 vs original: {sim_rec2_hlb:.3f}")
  print()
  print()





  country  = hdv()
  capital  = hdv()
  currency = hdv()

  usa = hdv()
  mex = hdv()
  hun = hdv()

  wdc = hdv()
  mxc = hdv()
  bud = hdv()

  usd = hdv()
  mxn = hdv()
  huf = hdv()

  usa_map = bundle(
    bind(country, usa),
    bind(capital, wdc),
    bind(currency, usd),
  )

  mex_map = bundle(
    bind(country, mex),
    bind(capital, mxc),
    bind(currency, mxn),
  )

  hun_map = bundle(
    bind(country, hun),
    bind(capital, bud),
    bind(currency, huf),
  )

  # What is the dollar of Mexico?
  query = unbind(mex_map, currency)
  print("Dollar of Mexico?")
  print("USD:", similarity(query, usd))
  print("MXN:", similarity(query, mxn))
  print("HUF:", similarity(query, huf))
  print()

  # What is the capital of Hungary?
  query = unbind(hun_map, capital)
  print("Capital of Hungary?")
  print("WDC:", similarity(query, wdc))
  print("MXC:", similarity(query, mxc))
  print("BUD:", similarity(query, bud))
  print()


