# llm generated

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import hadamard

def hlb_bind(a: np.ndarray, b: np.ndarray) -> np.ndarray:
  """Hadamard-derived Linear Binding (HLB) between two vectors a and b."""
  n = len(a)
  H = hadamard(n) / np.sqrt(n)
  A = H @ a
  B = H @ b
  C = A * B
  return H @ C

def hlb_unbind(a: np.ndarray, bound: np.ndarray) -> np.ndarray:
  """Inverse binding for HLB."""
  n = len(a)
  H = hadamard(n) / np.sqrt(n)
  A = H @ a
  C = H @ bound
  # Avoid divide-by-zero issues
  B_est = C / (A + 1e-9)
  return H @ B_est

# --- Example data -----------------------------------------------------------

np.random.seed(42)
a = np.random.randn(64)
b = np.random.randn(64)

# Bind and unbind
hlb_bound = hlb_bind(a, b)
b_reconstructed = hlb_unbind(a, hlb_bound)

# --- Visualization ----------------------------------------------------------

plt.figure(figsize=(14, 6))

plt.subplot(1, 3, 1)
plt.title("Original vector b")
plt.plot(b, color='steelblue')
plt.xlabel("Dimension index")
plt.ylabel("Value")
plt.grid(True)

plt.subplot(1, 3, 2)
plt.title("Bound vector (HLB(a,b))")
plt.plot(hlb_bound, color='darkorange')
plt.xlabel("Dimension index")
plt.grid(True)

plt.subplot(1, 3, 3)
plt.title("Recovered vector b′ from unbinding")
plt.plot(b, color='gray', linestyle='--', label='True b')
plt.plot(b_reconstructed, color='green', alpha=0.7, label='Recovered b′')
plt.xlabel("Dimension index")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Print reconstruction quality
cosine_similarity = np.dot(b, b_reconstructed) / (np.linalg.norm(b) * np.linalg.norm(b_reconstructed))
print(f"Cosine similarity between original and reconstructed b: {cosine_similarity:.4f}")
