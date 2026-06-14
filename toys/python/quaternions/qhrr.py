# Quarternion Holograph Reduced Representations (QHRR)
# Hamilton Holograph Reduced Representations (HHRR)

import numpy as np


def normalize_quaternions(hv):
  '''Normalize all quaternions to unit in a hypervector'''
  return hv / np.linalg.norm(hv, axis=-1, keepdims=True)

def new_hv(dimensions):
  '''Create a new random unit quaternion'''
  return normalize_quaternions(np.random.randn(dimensions, 4))

def inverse(q):
  '''The conjugate is an exact inverse for unit quaternions'''
  qc = q.copy()
  qc[..., 1:] *= -1
  return qc

def quaternion_multiply(q1, q2):
  '''Hamilton product'''
  w1, x1, y1, z1 = np.split(q1, 4, axis=-1)
  w2, x2, y2, z2 = np.split(q2, 4, axis=-1)
  return np.concatenate([
    w1*w2 - x1*x2 - y1*y2 - z1*z2,
    w1*x2 + x1*w2 + y1*z2 - z1*y2,
    w1*y2 - x1*z2 + y1*w2 + z1*x2,
    w1*z2 + x1*y2 - y1*x2 + z1*w2
  ], axis=-1)

def bind(hv1, hv2):
  '''Entangle two hypervector'''
  return normalize_quaternions(quaternion_multiply(hv1, hv2))

def unbind(bound, query):
  '''Unbind a query from a composite'''
  return normalize_quaternions(quaternion_multiply(inverse(query), bound))

def bundle(vectors):
  '''Superimpose multiple hypervector'''
  vectors = np.stack(vectors, axis=0)
  summed = np.sum(vectors, axis=0)
  return normalize_quaternions(summed)

def permute(hv, k=1):
  '''Cyclic shift'''
  return np.roll(hv, shift=k, axis=0)

def similarity(hv1, hv2):
  '''Compare how similar two hypervector are, -1 to 1'''
  return np.mean(np.sum(hv1*hv2, axis=-1))

def fraction_power_encoding(q, alpha):
  '''Fractional Power Encoding'''
  q = normalize_quaternions(q)
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
  '''Exhaustive nearest neighbor search'''
  similarities = {}
  for symbol, hv in codebook.items():
    similarities[symbol] = similarity(query, hv)
  best_symbol = max(similarities, key=similarities.get)
  return best_symbol, similarities


if __name__ == "__main__":
  np.random.seed(0)
  D = 10_000

  print("\n--- Hypervector generation ---")
  hv = new_hv(D)
  print("Shape:", hv.shape)
  print("Unit norm (first element):", np.linalg.norm(hv[0]))
  print("First element:", hv[0])

  print("\n--- Quaternion multiply + inverse test ---")
  q1 = new_hv(1)[0]
  q2 = new_hv(1)[0]
  prod = quaternion_multiply(q1, q2)
  recovered = quaternion_multiply(prod, inverse(q2))
  print("Recover q1:", np.allclose(q1, recovered, atol=1e-6))

  print("\n--- Binding / unbinding test ---")
  ROLE = new_hv(D)
  FILLER = new_hv(D)
  BOUND = bind(ROLE, FILLER)
  RECOVERED = unbind(BOUND, ROLE)
  print("Exact recovery (geometric):",
    similarity(FILLER, RECOVERED))

  print("\n--- Non-commutativity test ---")
  BOUND_AB = bind(ROLE, FILLER)
  BOUND_BA = bind(FILLER, ROLE)
  print("A⊗B != B⊗A:", not np.allclose(BOUND_AB, BOUND_BA))

  print("\n--- Bundling test ---")
  A = new_hv(D)
  B = new_hv(D)
  C = new_hv(D)
  BUNDLE = bundle([A, B, C])
  print("Bundle shape:", BUNDLE.shape)
  print("Bundle element is unit quaternion:",
    np.isclose(np.linalg.norm(BUNDLE[0]), 1.0))

  print("\n--- Fractional quaternion power test ---")
  half = fraction_power_encoding(ROLE, 0.5)
  recomposed = bind(half, half)
  print("Half ⊗ Half ≈ original:",
    similarity(recomposed, ROLE) > 0.999)

  print("\n--- Similarity test ---")
  print("Similarity identical:", similarity(ROLE, ROLE))
  print("Similarity random:", similarity(ROLE, FILLER))

  print("\n--- Permutation tests ---")
  PERM = permute(ROLE, 5)
  print("Cyclic shift permutation preserves norm:",
    np.isclose(np.linalg.norm(PERM[0]), 1.0))

  p = new_hv(D)
  conjugated = quaternion_multiply(
    quaternion_multiply(ROLE, p),
    inverse(p)
  )

  print("Conjugation changes absolute similarity:",
    similarity(ROLE, conjugated) < 0.1)

  print("\n--- Cleanup / nearest neighbor test ---")
  codebook = {
    "A": new_hv(D),
    "B": new_hv(D),
    "C": new_hv(D),
  }

  query = bind(codebook["A"], codebook["B"])
  recovered = unbind(query, codebook["A"])
  symbol, similarities = cleanup(recovered, codebook)

  print("Recovered symbol should be B:", symbol)
  print("Similarities:", similarities)
