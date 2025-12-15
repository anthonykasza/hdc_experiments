import numpy as np


def random_unitary(m: int) -> np.ndarray:
  z = (np.random.randn(m, m) + 1j * np.random.randn(m, m)) / np.sqrt(2)
  q, r = np.linalg.qr(z)
  d = np.diag(r)
  return q * (d / np.abs(d))


def polar_normalize(mats: np.ndarray) -> np.ndarray:
  """Project each matrix back to the closest unitary (polar decomposition)."""
  out = np.empty_like(mats)
  for i in range(mats.shape[0]):
    u, _, vh = np.linalg.svd(mats[i])
    out[i] = u @ vh
  return out


def hdv(D: int = 10000, m: int = 2) -> np.ndarray:
  H = np.zeros((D, m, m), dtype=np.complex128)

  for j in range(D):
    Q = random_unitary(m)
    theta = np.random.uniform(0, 2 * np.pi, size=m)
    Lambda = np.diag(np.exp(1j * theta))
    H[j] = Q @ Lambda

  return H


def bind(a, b):
  return np.einsum("dij,djk->dik", a, b)


def unbind(a, b):
  b_inv = b.conj().transpose(0, 2, 1)
  return np.einsum("dij,djk->dik", a, b_inv)


def bundle(*vectors):
  summed = np.sum(vectors, axis=0)
  return polar_normalize(summed)


def similarity(a, b):
  D, m, _ = a.shape
  sim = 0.0
  for j in range(D):
    sim += np.trace(a[j] @ b[j].conj().T)
  return np.real(sim) / (D * m)



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
