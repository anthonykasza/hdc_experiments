import numpy as np
import matplotlib.pyplot as plt

from qhrr import *



def mean_distance(a, b):
  return np.mean(similarity(a, b))

EPS = 1e-8
def quaternion_log(q):
  q = normalize_quaternions(q)

  w = np.clip(q[..., 0], -1.0, 1.0)
  v = q[..., 1:]

  theta = np.arccos(w)
  sin_theta = np.sin(theta)

  small = sin_theta < EPS

  axis = np.zeros_like(v)
  axis[~small] = v[~small] / (sin_theta[~small, None] + EPS)
  axis[small] = np.array([1.0, 0.0, 0.0])

  return axis * theta[..., None]


def quaternion_exp(v):
  theta = np.linalg.norm(v, axis=-1, keepdims=True)

  small = theta < EPS

  axis = np.zeros_like(v)
  axis[~small[..., 0]] = v[~small[..., 0]] / (theta[~small[..., 0]] + EPS)
  axis[small[..., 0]] = np.array([1.0, 0.0, 0.0])

  w = np.cos(theta)
  xyz = axis * np.sin(theta)

  q = np.concatenate([w, xyz], axis=-1)
  return normalize_quaternions(q)


def lie_bundle(vectors):
  logs = np.stack([quaternion_log(v) for v in vectors], axis=0)
  mean_log = np.mean(logs, axis=0)
  return normalize_quaternions(quaternion_exp(mean_log))


# ============================================================
# EXPERIMENT
# ============================================================

np.random.seed(42)

D = 5000
N = 20
codebook = [new_hv(D) for _ in range(N)]

xs = list(range(2, N + 1))

results_qhrr = []
results_lie = []
results_noise = []

trials = 10

# ============================================================
# MAIN LOOP
# ============================================================

for X in xs:

  if X == 0:
    results_qhrr.append(0.0)
    results_lie.append(0.0)
    results_noise.append(0.0)
    continue

  d_qhrr = []
  d_lie = []
  d_noise = []

  for _ in range(trials):

    idx = np.random.choice(N, X, replace=False)
    selected = [codebook[i] for i in idx]

    # ----------------------------
    # QHRR bundle
    # ----------------------------
    bundle_q = bundle(selected)
    d_qhrr.append(np.mean([mean_distance(bundle_q, v) for v in selected]))

    # ----------------------------
    # Lie bundle
    # ----------------------------
    bundle_l = lie_bundle(selected)
    d_lie.append(np.mean([mean_distance(bundle_l, v) for v in selected]))

    # ----------------------------
    # NOISE BASELINE
    # ----------------------------
    random_vec = new_hv(D)
    d_noise.append(np.mean([mean_distance(random_vec, v) for v in selected]))

  results_qhrr.append(np.mean(d_qhrr))
  results_lie.append(np.mean(d_lie))
  results_noise.append(np.mean(d_noise))


# ============================================================
# PLOT WITH PI-SCALED AXIS
# ============================================================

plt.figure(figsize=(9, 6))

plt.plot(xs, results_qhrr, marker='o', label="QHRR")
plt.plot(xs, results_lie, marker='o', label="Lie algebra")
plt.plot(xs, results_noise, linestyle='--', label="Random hypervector (noise baseline)")


plt.xticks(range(0, N + 1))

plt.xlabel("Number of bundled hypervectors")
plt.ylabel("Similarity")
plt.title("QHRR vs Lie Algebra Bundling")
plt.grid(True)
plt.legend()

plt.show()
