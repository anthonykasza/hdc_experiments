# Binding and querying/recovering are possible with small vectors too.


import numpy as np

def ldv():
  """Low-dimensional vector (unit quaternion)"""
  q = np.random.randn(4)
  return q / np.linalg.norm(q)

def bind(q1, q2):
  """Quaternion multiply"""
  w1, x1, y1, z1 = q1
  w2, x2, y2, z2 = q2
  return np.array([
    w1*w2 - x1*x2 - y1*y2 - z1*z2,
    w1*x2 + x1*w2 + y1*z2 - z1*y2,
    w1*y2 - x1*z2 + y1*w2 + z1*x2,
    w1*z2 + x1*y2 - y1*x2 + z1*w2
  ])

def inverse(q):
  """Quaternion inverse (conjugate for unit quaternions)"""
  return np.array([q[0], -q[1], -q[2], -q[3]])


ROLE = ldv()
FILLER = ldv()
BOUND = bind(ROLE, FILLER)
RECOVERED = bind(inverse(ROLE), BOUND)
print("Recovered ?= filler:", np.allclose(FILLER, RECOVERED))

