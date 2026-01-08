# Randsel and Concat are the same thing. They enable weighting.
# Neither requires clipping nor normalization.
# Both give the same results regardless of hv element type/range.
# Both are less robust than sum+clip. Perhaps they are faster?


import numpy as np
from numpy.linalg import norm



def hdv(n=10_000, all=None):
  if all is not None:
    return np.full((1, n), all).flatten()
  return np.random.choice([-1, 1], size=n)

def sim(h1, h2):
  if norm(h1) == 0 or norm(h2) == 0:
    return 0
  return abs(np.dot(h1, h2) / (norm(h1) * norm(h2)))


def sumclip_bundle(*hvs):
  return np.sign(np.sum(hvs, axis=0))

def randsel_bundle(*hvs):
  acc = hdv(all=0)
  for i in range(len(acc)):
    hv = hvs[np.random.randint(len(hvs))]
    acc[i] = hv[i]
  return acc

def concat_bundle(*hvs):
  acc = hdv(all=0)
  elments_per_hv = int(len(acc) / len(hvs))
  for idx in range(len(hvs)):
    start = idx * elments_per_hv
    stop = start + elments_per_hv
    acc[start:stop] = hvs[idx][start:stop]

  # if len(acc) isn't evenly divisible by the
  #  count of constituent hypervectors, then
  #  just fill the remaining acc indices with
  #  values from the last constituent
  if len(acc) / len(hvs) > elments_per_hv:
    remain = len(acc) - (elments_per_hv * len(hvs))
    acc[-remain] = hvs[-1][-remain]

  return acc


def randsel_weighted_bundle(weights, *hvs):
  acc = hdv(n=len(hvs[0]), all=0)
  n = len(hvs)
  for i in range(len(acc)):
    idx = int(np.random.choice(n, p=weights))
    hv = hvs[idx]
    acc[i] = hv[i]
  return acc

def normalize_weights(w):
  return [each / sum(w) for each in w]


NUM_TRIALS = 25
NUM_SIGNALS = 5
# len(WEIGHTS) must equal NUM_SIGNALS
WEIGHTS = normalize_weights([0, 0, 0, 0, 1,])

rb_results = []
cb_results = []
sb_results = []
wb_results = []

rb_noise = []
cb_noise = []
sb_noise = []
wb_noise = []


for i in range(NUM_TRIALS):
  signals = [hdv() for i in range(NUM_SIGNALS)]
  noise = hdv()

  rb = randsel_bundle(*signals)
  cb = concat_bundle(*signals)
  sb = sumclip_bundle(*signals)
  wb = randsel_weighted_bundle(WEIGHTS, *signals)

  rb_results.append([sim(signal, rb) for signal in signals])
  cb_results.append([sim(signal, cb) for signal in signals])
  sb_results.append([sim(signal, sb) for signal in signals])
  wb_results.append([sim(signal, wb) for signal in signals])

  rb_noise.append(sim(noise, rb))
  cb_noise.append(sim(noise, cb))
  sb_noise.append(sim(noise, sb))
  wb_noise.append(sim(noise, wb))


print("Ave sim of bundle to constituents: Randsel")
for s_idx in range(NUM_SIGNALS):
  x = np.mean([rb_results[trial_idx][s_idx] for trial_idx in range(NUM_TRIALS)])
  print('  signal', s_idx, x)
print('  noise', np.mean(rb_noise))
print()

print("Ave sim of bundle to constituents: Concatenation")
for s_idx in range(NUM_SIGNALS):
  x = np.mean([cb_results[trial_idx][s_idx] for trial_idx in range(NUM_TRIALS)])
  print('  signal', s_idx, x)
print('  noise', np.mean(cb_noise))
print()

print("Ave sim of bundle to constituents: Sum and Clip")
for s_idx in range(NUM_SIGNALS):
  x = np.mean([sb_results[trial_idx][s_idx] for trial_idx in range(NUM_TRIALS)])
  print('  signal', s_idx, x)
print('  noise', np.mean(sb_noise))
print()

print("Ave sim of bundle to constituents: Randsel weighted")
print(WEIGHTS)
for s_idx in range(NUM_SIGNALS):
  x = np.mean([wb_results[trial_idx][s_idx] for trial_idx in range(NUM_TRIALS)])
  print('  signal', s_idx, x)
print('  noise', np.mean(wb_noise))
print()
