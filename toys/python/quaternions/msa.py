import numpy as np



def random_unitary(m):
  """Haar-like random unitary via QR decomposition."""
  z = np.random.randn(m, m) + 1j * np.random.randn(m, m)
  q, r = np.linalg.qr(z)
  return q


def normalize_unitary(U):
  """Project matrix back to unitary group (polar decomposition)."""
  Uu, _, Vh = np.linalg.svd(U)
  return Uu @ Vh


def batch_svd_project(M):
  """
  Project each (m,m) matrix in (D,m,m) back to unitary group.
  """
  D = M.shape[0]
  U = np.zeros_like(M)
  for i in range(D):
    Ui, _, Vhi = np.linalg.svd(M[i])
    U[i] = Ui @ Vhi
  return U


def to_variance(kappa):
  return (1.0 / np.clip(kappa, 1e-8, 1.0)) - 1.0


def to_kappa(var):
  return 1.0 / (1.0 + var)



def new_hv(D, m, kappa=1.0):
  """
  Hypervector:
    U: (D, m, m) unitary matrices
    kappa: (D,) concentration per slot
  """
  U = np.stack([random_unitary(m) for _ in range(D)], axis=0)
  k = np.full((D,), kappa, dtype=float)
  return U, k

import numpy as np

def bind(A, B, alpha=1.0, beta=0.5):
    UA, kA = A
    UB, kB = B

    # U(m) group operation
    U = np.matmul(UA, UB)

    # confidence propagation
    k_base = np.sqrt(kA * kB)

    alignment = np.real(np.sum(np.conj(UA) * UB, axis=(1, 2))) / UA.shape[1]
    alignment = np.clip(alignment, 0.0, 1.0)

    k_reinforce = kA * kB * alignment

    k = alpha * k_base + beta * k_reinforce
    k = np.tanh(k)

    return U, k


def unbind(A, B, alpha=1.0, beta=0.5):
    UA, kA = A
    UB, kB = B

    # group inverse operation
    UB_inv = np.conj(UB).transpose(0, 2, 1)
    U = np.matmul(UA, UB_inv)

    # confidence propagation (symmetric, but penalizes weak factors)
    k_base = np.sqrt(kA * kB)

    alignment = np.real(np.sum(np.conj(UA) * UB, axis=(1, 2))) / UA.shape[1]
    alignment = np.clip(alignment, 0.0, 1.0)

    k_recover = kA * kB * alignment

    k = alpha * k_base + beta * k_recover
    k = np.tanh(k)

    return U, k



def bundle(vectors):
  """
  """

  if len(vectors) == 0:
    raise ValueError("Cannot bundle empty list")

  Us = np.stack([v[0] for v in vectors], axis=0)   # (N, D, m, m)
  ks = np.stack([v[1] for v in vectors], axis=0)   # (N, D)
  ks_exp = ks[:, :, None, None]

  # weighted sum over samples
  M = np.sum(Us * ks_exp, axis=0)  # (D, m, m)

  # project each slot back to unitary
  U = batch_svd_project(M)
  strength = np.linalg.norm(M, axis=(1, 2))
  weight_sum = np.sum(ks, axis=0)

  kappa = strength / (weight_sum + 1e-12)

  # clip for stability
  kappa = np.clip(kappa, 1e-6, 1.0)

  return U, kappa



def similarity(A, B):
  UA, kA = A
  UB, kB = B

  # per-slot complex inner product
  sim = np.real(np.sum(np.conj(UA) * UB, axis=(1, 2)))  # (D,)

  # combine confidence from both sides
  w = kA * kB  # joint reliability

  # normalize by matrix size
  sim = sim / UA.shape[1]

  return np.sum(w * sim) / (np.sum(w) + 1e-12)


def permute(X, k=1):
  U, c = X
  return np.roll(U, shift=k, axis=0), np.roll(c, shift=k, axis=0)



if __name__ == "__main__":

  D = 256
  m = 8

  A = new_hv(D, m)
  B = new_hv(D, m)
  C = new_hv(D, m)

  # bundling test
  BUNDLE = bundle([A, A, B, C])
  BUNDLE = bundle([BUNDLE, A, B])

  print("Bundle κ mean:", np.mean(BUNDLE[1]))
  print("Similarity to A:", similarity(BUNDLE, A))
  print("Similarity to B:", similarity(BUNDLE, B))
  print("Similarity to C:", similarity(BUNDLE, C))
  print("Similarity to noise:", similarity(BUNDLE, new_hv(D, m)))


# --- binding test ---
  AB = bind(A, B)

  print("\n--- BIND TEST ---")
  print("sim(AB, A⊛B):", similarity(AB, AB))
  print("sim(AB, A):", similarity(AB, A))
  print("sim(AB, B):", similarity(AB, B))

  # --- unbind test (recover A from AB using B) ---
  A_rec = unbind(AB, B)

  print("\n--- UNBIND TEST ---")
  print("sim(A_rec, A):", similarity(A_rec, A))
  print("sim(A_rec, B):", similarity(A_rec, B))

  # --- consistency loop test ---
  ABA = bind(A_rec, B)

  print("\n--- ROUNDTRIP TEST ---")
  print("sim(ABA, AB):", similarity(ABA, AB))
