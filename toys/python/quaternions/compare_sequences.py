# QHRR's superposition is weak but its binding
#  is non-commutative making it potentially useful
#  for sequences.

# TODO: consider randsel instead of sum+normalize


import numpy as np
from qhrr import *

# ============================================================
# FHRR (Fourier HRR) with positional permutation
# ============================================================

def fhrr_random(D):
  theta = np.random.uniform(0, 2 * np.pi, size=D)
  return np.exp(1j * theta)

def fhrr_bind(a, b):
  return a * b

def fhrr_unbind(bound, key):
  return bound * np.conj(key)

def fhrr_bundle(vs):
  s = np.sum(vs, axis=0)
  return s / np.abs(s)

def fhrr_similarity(a, b):
  return np.real(np.vdot(a, b)) / len(a)

def fhrr_permute(v, shift):
  return np.roll(v, shift)  # simple circular permutation



if __name__ == "__main__":
  np.random.seed(42)
  D = 5000
  max_seq_length = 300
  seq_length_step = 10
  trials = 10

  print("--- FHRR (permute) vs QHRR sequence encoding ---")
  print("SeqLen | FHRR avg sim | QHRR avg sim")

  for seq_length in range(5, max_seq_length + 1, seq_length_step):
    fhrr_sims = []
    qhrr_sims = []

    for _ in range(trials):
      # FHRR with positional permutation
      roles_fhrr = [fhrr_random(D) for _ in range(seq_length)]
      fillers_fhrr = [fhrr_random(D) for _ in range(seq_length)]
      bound_fhrr = [fhrr_bind(f, fhrr_permute(r, i)) for i, (r, f) in enumerate(zip(roles_fhrr, fillers_fhrr))]
      memory_fhrr = fhrr_bundle(bound_fhrr)
      recovered_fhrr = fhrr_unbind(memory_fhrr, fhrr_permute(roles_fhrr[0], 0))
      fhrr_sims.append(fhrr_similarity(recovered_fhrr, fillers_fhrr[0]))

      # QHRR sequential binding
      roles_qhrr = [qhrr_random(D) for _ in range(seq_length)]
      fillers_qhrr = [qhrr_random(D) for _ in range(seq_length)]
      memory_qhrr = fillers_qhrr[0]
      for i in range(1, seq_length):
        memory_qhrr = qhrr_bind(memory_qhrr, roles_qhrr[i])
      query_qhrr = memory_qhrr
      for i in reversed(range(1, seq_length)):
        query_qhrr = qhrr_unbind(query_qhrr, roles_qhrr[i])
      qhrr_sims.append(qhrr_similarity(query_qhrr, fillers_qhrr[0]))

    print(f"{seq_length:6d} | {np.mean(fhrr_sims):12.4f} | {np.mean(qhrr_sims):12.4f}")
