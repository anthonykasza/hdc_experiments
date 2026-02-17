import numpy as np


# ------------------------------------------------------------
# Hypervector creation
# ------------------------------------------------------------

def new_hv(dims, block_size, kappa=1.0, rng=None):
  """
  Create a new random hypervector.

  Returns:
  mu: integer phases in [0, block_size)
  kappa: concentration values in (0, 1)

  μ is only meaningful if κ>0; otherwise μ is arbitrary.
  """
  rng = np.random.default_rng(rng)
  mu = rng.integers(0, block_size, size=dims)
  kappa = np.clip(float(kappa), 0.0, 1.0)
  kappa_arr = np.full(dims, kappa)
  return mu, kappa_arr


# ------------------------------------------------------------
# Binding (circular addition)
# ------------------------------------------------------------

def bind(hvs, block_size, eps=1e-12):
    """
    Bind hypervectors via circular phase addition.
    Uncertainty propagates via variance addition.

    κ is interpreted as:
        κ = 1 / (1 + σ²)

    So:
        σ² = 1/κ - 1
        σ²_total = sum σ²
        κ_new = 1 / (1 + σ²_total)
    """
    mus = np.stack([hv[0] for hv in hvs], axis=0)
    kappas = np.stack([hv[1] for hv in hvs], axis=0)

    # --- Phase addition ---
    mu_sum = np.mod(np.sum(mus, axis=0), block_size)

    # --- Convert κ -> variance ---
    kappas = np.clip(kappas, eps, 1.0)
    variances = (1.0 / kappas) - 1.0

    # --- Variance addition ---
    var_sum = np.sum(variances, axis=0)

    # --- Convert back to κ ---
    kappa_new = 1.0 / (1.0 + var_sum)

    return mu_sum, kappa_new


def unbind(h1, h2, block_size, eps=1e-12):
    """
    Circular subtraction with variance addition.

    Phase:
        μ_new = μ1 - μ2 mod block_size

    Variance:
        σ²_new = σ²1 + σ²2
    """
    mu1, kappa1 = h1
    mu2, kappa2 = h2

    # --- Phase subtraction ---
    mu_diff = (mu1 - mu2) % block_size

    # --- Convert κ -> variance ---
    kappa1 = np.clip(kappa1, eps, 1.0)
    kappa2 = np.clip(kappa2, eps, 1.0)

    var1 = (1.0 / kappa1) - 1.0
    var2 = (1.0 / kappa2) - 1.0

    # --- Variance addition ---
    var_sum = var1 + var2

    # --- Convert back to κ ---
    kappa_new = 1.0 / (1.0 + var_sum)

    return mu_diff, kappa_new


def inverse(hv, block_size):
  """
  Reverse polarity (circular negation).
  """
  mu, kappa = hv
  return (-mu) % block_size, kappa


# ------------------------------------------------------------
# Bundling (κ-weighted circular mean)
# ------------------------------------------------------------

def bundle(hvs, block_size):
  """
  κ-weighted circular mean (von Mises-like fusion).

  Geometry:
  μ = arg( sum_i κ_i * exp(jθ_i) )

  Returns:
  mu:  discrete circular mean
  kappa: agreement-based concentration
  """
  mus = np.stack([hv[0] for hv in hvs], axis=0)  # (N, D)
  kappas = np.stack([hv[1] for hv in hvs], axis=0)   # (N, D)

  # Convert discrete phase to radians
  angles = 2 * np.pi * mus / block_size

  # κ-weighted phasors
  weighted_phasors = kappas * np.exp(1j * angles)

  # Sum phasors
  phasor_sum = np.sum(weighted_phasors, axis=0)

  # Mean angle
  mean_angle = np.angle(phasor_sum)

  # Convert back to discrete phase
  scaled = mean_angle * block_size / (2 * np.pi)
  mu = np.mod(np.floor(scaled + 0.5), block_size).astype(int)

  # Adjust κ for quantization error
  theta_quantized = 2 * np.pi * mu / block_size
  epsilon = np.angle(np.exp(1j*(mean_angle - theta_quantized)))

  # Agreement-based κ (stronger when aligned)
  R = np.abs(phasor_sum)
  total_weight = np.sum(kappas, axis=0)

  # projection onto quantized direction
  proj = R * np.cos(epsilon)
  proj = np.maximum(proj, 0.0)

  # Avoid division by zero
  kappa = np.divide(
    proj,
    total_weight,
    out=np.zeros_like(R),
    where=total_weight > 1e-12
  )

  return mu, kappa


# ------------------------------------------------------------
# Similarity (κ-weighted circular cosine)
# ------------------------------------------------------------
def similarity(h1, h2, block_size, eps=1e-12):
    """
    Expected cosine similarity under small-noise circular model.

    κ interpreted as:
        κ = 1 / (1 + σ²)

    Similarity:
        E[cos(θ1 - θ2)] ≈ κ1 κ2 cos(Δμ)

    Returns value in [0,1]
    """
    mu1, kappa1 = h1
    mu2, kappa2 = h2

    # Convert discrete phase to radians
    theta1 = 2 * np.pi * mu1 / block_size
    theta2 = 2 * np.pi * mu2 / block_size

    delta = theta1 - theta2

    # Expected cosine under uncertainty
    expected_cos = kappa1 * kappa2 * np.cos(delta)

    # Mean over dimensions
    sim = np.mean(expected_cos)

    # Map from [-1,1] to [0,1]
    return (sim + 1.0) / 2.0
