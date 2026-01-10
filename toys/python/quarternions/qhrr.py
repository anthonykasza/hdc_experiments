# Quarternion Holograph Reduced Representations


import numpy as np

def normalize_quaternion(q):
  return q / np.linalg.norm(q, axis=-1, keepdims=True)

def random_unit_quaternion(shape):
  return normalize_quaternion(np.random.randn(*shape, 4))

def quaternion_conjugate(q):
  qc = q.copy()
  qc[..., 1:] *= -1
  return qc

def quaternion_multiply(q1, q2):
  w1, x1, y1, z1 = np.split(q1, 4, axis=-1)
  w2, x2, y2, z2 = np.split(q2, 4, axis=-1)
  return np.concatenate([
    w1*w2 - x1*x2 - y1*y2 - z1*z2,
    w1*x2 + x1*w2 + y1*z2 - z1*y2,
    w1*y2 - x1*z2 + y1*w2 + z1*x2,
    w1*z2 + x1*y2 - y1*x2 + z1*w2
  ], axis=-1)

def qhrr_random(D):
  return random_unit_quaternion((D,))

def qhrr_bind(a, b):
  return normalize_quaternion(quaternion_multiply(a, b))

def qhrr_unbind(bound, key):
  return normalize_quaternion(quaternion_multiply(bound, quaternion_conjugate(key)))

def qhrr_bundle(vectors):
  vectors = np.stack(vectors, axis=0)  # (K, D, 4)
  summed = np.sum(vectors, axis=0)   # (D, 4)
  return normalize_quaternion(summed)

def quaternion_geodesic_distance(q1, q2):
  dot = np.sum(q1 * q2, axis=-1)
  dot = np.clip(np.abs(dot), -1.0, 1.0)
  return 2.0 * np.arccos(dot)

def mean_geodesic_distance(hv1, hv2):
  return np.mean(quaternion_geodesic_distance(hv1, hv2))

def permute_roll(hv, k=1):
  return np.roll(hv, shift=k, axis=0)

def permute_conjugation(hv, p):
  return quaternion_multiply(
    quaternion_multiply(p, hv),
    quaternion_conjugate(p)
  )

def qhrr_similarity(hv1, hv2):
  return 1.0 - mean_geodesic_distance(hv1, hv2) / np.pi

def quaternion_power(q, alpha):
  '''power encoding'''
  q = normalize_quaternion(q)

  w = np.clip(q[..., 0], -1.0, 1.0)
  v = q[..., 1:]

  theta = 2.0 * np.arccos(w)
  sin_half = np.sqrt(1.0 - w*w)

  small = sin_half < 1e-8

  axis = np.zeros_like(v)
  axis[~small] = v[~small] / sin_half[~small, None]
  axis[small] = np.array([1.0, 0.0, 0.0])

  new_theta = alpha * theta
  half = new_theta / 2.0

  w_new = np.cos(half)
  v_new = axis * np.sin(half)[..., None]

  return np.concatenate([w_new[..., None], v_new], axis=-1)

def cleanup(query, codebook):
  distances = {}
  for symbol, hv in codebook.items():
    distances[symbol] = mean_geodesic_distance(query, hv)

  best_symbol = min(distances, key=distances.get)
  return best_symbol, distances



if __name__ == "__main__":
  np.random.seed(0)
  D = 10_000

  print("\n--- Hypervector generation ---")
  hv = qhrr_random(D)
  print("Shape:", hv.shape)
  print("Unit norm (first element):", np.linalg.norm(hv[0]))
  print("First element:", hv[0])

  print("\n--- Quaternion multiply + inverse test ---")
  q1 = random_unit_quaternion((1,))[0]
  q2 = random_unit_quaternion((1,))[0]
  prod = quaternion_multiply(q1, q2)
  recovered = quaternion_multiply(prod, quaternion_conjugate(q2))
  print("Recover q1:", np.allclose(q1, recovered, atol=1e-6))

  print("\n--- Binding / unbinding test ---")
  ROLE = qhrr_random(D)
  FILLER = qhrr_random(D)
  BOUND = qhrr_bind(ROLE, FILLER)
  RECOVERED = qhrr_unbind(BOUND, ROLE)
  print("Exact recovery (geometric):",
    qhrr_similarity(FILLER, RECOVERED) > 0.999999)

  print("\n--- Non-commutativity test ---")
  BOUND_AB = qhrr_bind(ROLE, FILLER)
  BOUND_BA = qhrr_bind(FILLER, ROLE)
  print("A⊗B != B⊗A:", not np.allclose(BOUND_AB, BOUND_BA))

  print("\n--- Bundling test ---")
  A = qhrr_random(D)
  B = qhrr_random(D)
  C = qhrr_random(D)
  BUNDLE = qhrr_bundle([A, B, C])
  print("Bundle shape:", BUNDLE.shape)
  print("Bundle element is unit quaternion:",
    np.isclose(np.linalg.norm(BUNDLE[0]), 1.0))

  print("\n--- Fractional quaternion power test ---")
  half = quaternion_power(ROLE, 0.5)
  recomposed = qhrr_bind(half, half)
  print("Half ⊗ Half ≈ original:",
    qhrr_similarity(recomposed, ROLE) > 0.999)

  print("\n--- Geodesic distance & similarity test ---")
  print("Distance identical:", mean_geodesic_distance(ROLE, ROLE))
  print("Similarity identical:", qhrr_similarity(ROLE, ROLE))
  print("Similarity random:", qhrr_similarity(ROLE, FILLER))

  print("\n--- Permutation tests ---")
  rolled = permute_roll(ROLE, 5)
  print("Roll preserves norm:",
    np.isclose(np.linalg.norm(rolled[0]), 1.0))

  p = random_unit_quaternion((D,))
  conjugated = permute_conjugation(ROLE, p)

  print("Conjugation changes absolute similarity:",
    qhrr_similarity(ROLE, conjugated) < 0.1)

  print("\n--- Cleanup / nearest neighbor test ---")
  codebook = {
  "A": qhrr_random(D),
  "B": qhrr_random(D),
  "C": qhrr_random(D),
  }

  query = qhrr_bind(codebook["A"], codebook["B"])
  recovered = qhrr_unbind(query, codebook["A"])
  symbol, distances = cleanup(recovered, codebook)

  print("Recovered symbol:", symbol)
  print("Distances:", distances)
