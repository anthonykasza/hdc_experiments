import cv2
import numpy as np
import matplotlib.pyplot as plt

POLE = 127.0


# ------------------------------------------------------------
# Utility
# ------------------------------------------------------------

def load_gray(path):
  img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
  if img is None:
    raise FileNotFoundError(path)
  return img


# ------------------------------------------------------------
# FT-based stabilizer
# ------------------------------------------------------------

def spectral_whiten(img):
  img = img.astype(np.float32)

  # remove DC bias
  img -= img.mean()

  # FFT
  F = np.fft.fft2(img)
  F = np.fft.fftshift(F)

  h, w = img.shape

  fy = np.fft.fftfreq(h)
  fx = np.fft.fftfreq(w)
  FX, FY = np.meshgrid(fx, fy)

  R = np.sqrt(FX**2 + FY**2)
  eps = 1e-6

  # 1/f whitening approximation
  whitening = R + eps
  whitening = np.fft.fftshift(whitening)

  F = F * whitening

  # inverse FFT
  F = np.fft.ifftshift(F)
  x = np.real(np.fft.ifft2(F))

  # normalize
  x -= x.mean()
  x /= (x.std() + 1e-6)

  return x


# ------------------------------------------------------------
# VSA stabilizer
# ------------------------------------------------------------

def stabilize(img):
  x = spectral_whiten(img)

  # scale into VSA range
  x *= POLE / 3.0
  x = np.clip(x, -POLE, POLE)

  return x.astype(np.float32)


# ------------------------------------------------------------
# Display helper
# ------------------------------------------------------------

def to_image(x):
  return np.clip(
    (x + POLE) * (255.0 / (2.0 * POLE)),
    0,
    255
  ).astype(np.uint8)


# ------------------------------------------------------------
# HLB operations
# ------------------------------------------------------------

def identity(shape):
  return np.ones(shape, dtype=np.float32) * POLE


def empty(shape):
  return np.zeros(shape, dtype=np.float32)


def bundle(a, b):
  return np.clip(a + b, -POLE, POLE)


def bind(a, b):
  return (a * b) / POLE


def inverse(a):
  eps = 1e-6
  return POLE / np.where(np.abs(a) < eps, eps, a)


def cosine_similarity(a, b):
  aa = a.ravel()
  bb = b.ravel()

  return np.dot(aa, bb) / (
    np.linalg.norm(aa) * np.linalg.norm(bb)
  )


def make_levels(
  levels: int,
  hv1: np.ndarray,
  hv2: np.ndarray,
) -> dict[int, np.ndarray]:
  """
  Generate intermediate hypervectors while preserving the 2-D spatial layout.

  Manhattan moves are still applied in random order, but coordinates remain
  in image space rather than being flattened, producing much smoother visual
  transitions.
  """

  hv1 = hv1.astype(np.int16, copy=False)
  hv2 = hv2.astype(np.int16, copy=False)

  delta = hv2 - hv1

  # Pixels that differ
  ys, xs = np.nonzero(delta)

  if len(ys) == 0:
    return {i: hv1.copy() for i in range(levels)}

  counts = np.abs(delta[ys, xs]).astype(int)
  signs = np.sign(delta[ys, xs]).astype(np.int16)

  move_y = np.repeat(ys, counts)
  move_x = np.repeat(xs, counts)
  move_sign = np.repeat(signs, counts)

  total_work = len(move_y)

  perm = np.random.permutation(total_work)

  move_y = move_y[perm]
  move_x = move_x[perm]
  move_sign = move_sign[perm]

  hyperspace = {}

  current = hv1.copy()

  hyperspace[0] = current.copy()
  prev_work = 0

  for level in range(1, levels):

    target_work = round(level * total_work / (levels - 1))
    n_new = target_work - prev_work

    if n_new > 0:
      ys_batch = move_y[prev_work:target_work]
      xs_batch = move_x[prev_work:target_work]
      sign_batch = move_sign[prev_work:target_work]

      np.add.at(current, (ys_batch, xs_batch), sign_batch)

    hyperspace[level] = current.copy()
    prev_work = target_work

  return hyperspace


# ------------------------------------------------------------
# Tests
# ------------------------------------------------------------

raw_pen = load_gray("../images/pen.jpg")
raw_shoes = load_gray("../images/shoes.jpg")
raw_noise = load_gray("../images/noise.jpg")
#raw_noise = load_gray("./noise_u.jpg")

pen = stabilize(raw_pen)
shoes = stabilize(raw_shoes)
noise = stabilize(raw_noise)

print("\n========== Cosine similarities ==========")
print("pen   vs shoes :", cosine_similarity(pen, shoes))
print("pen   vs noise :", cosine_similarity(pen, noise))
print("shoes vs noise :", cosine_similarity(shoes, noise))


# ------------------------------------------------------------
# Bundle
# ------------------------------------------------------------

bundle_ps = bundle(pen, shoes)
bundle_pn = bundle(pen, noise)

print("\n========== Bundle ==========")
print("bundle(pen, shoes) → pen   :", cosine_similarity(bundle_ps, pen))
print("bundle(pen, shoes) → shoes :", cosine_similarity(bundle_ps, shoes))
print("bundle(pen, shoes) → noise :", cosine_similarity(bundle_ps, noise))
print()
print("bundle(pen, noise) → pen   :", cosine_similarity(bundle_pn, pen))
print("bundle(pen, noise) → noise :", cosine_similarity(bundle_pn, noise))
print("bundle(pen, noise) → shoes :", cosine_similarity(bundle_pn, shoes))


# ------------------------------------------------------------
# Bind
# ------------------------------------------------------------
# binding only works because the images have distribution
#  which is symmetric around it's center. if we were to use
#  a stabilization function, such as a high-boost sharpening filter
#  the resulting images would not have a symmetric distribution
#  of pixel values. they would bundle as expected but they
#  wouldn't behave as expected under binding. the symmetry in the
#  distribution of symbol element values is a requirement for
#  element-wise multiplication to "work" as a binding operator.

bind_ps = bind(pen, shoes)

print("\n========== Bind ==========")
print("bind(pen, shoes) → pen   :", cosine_similarity(bind_ps, pen))
print("bind(pen, shoes) → shoes :", cosine_similarity(bind_ps, shoes))
print("bind(pen, shoes) → noise :", cosine_similarity(bind_ps, noise))


# ------------------------------------------------------------
# Unbind
# ------------------------------------------------------------

recover_pen = bind(bind_ps, inverse(shoes))
recover_shoes = bind(bind_ps, inverse(pen))

print("\n========== Recovery ==========")
print("Recovered pen similarity should be high :", cosine_similarity(recover_pen, pen))
print("Recovered shoes similarity should be high :", cosine_similarity(recover_shoes, shoes))
print("Recovered noise similarity should be low :", cosine_similarity(recover_shoes, noise))




# ------------------------------------------------------------
# Raw vs Stabilized Images
# ------------------------------------------------------------

fig, ax = plt.subplots(3, 2, figsize=(8, 10))

pairs = [
    ("Pen", raw_pen, pen),
    ("Shoes", raw_shoes, shoes),
    ("Noise", raw_noise, noise),
]

for r, (name, raw, stable) in enumerate(pairs):

    ax[r, 0].imshow(raw, cmap="gray", vmin=0, vmax=255)
    ax[r, 0].set_title(f"Raw {name}")

    ax[r, 1].imshow(to_image(stable), cmap="gray", vmin=0, vmax=255)
    ax[r, 1].set_title(f"Stabilized {name}")

    ax[r, 0].axis("off")
    ax[r, 1].axis("off")

plt.tight_layout()
plt.savefig("raw_to_stab.jpg")


# ------------------------------------------------------------
# Visualization (FIGURE 1: 3x3 layout as requested)
# ------------------------------------------------------------

fig1, ax = plt.subplots(3, 3, figsize=(14, 12))

# Row 1: pen / noise / bundle(pen, noise)
ax[0,0].imshow(to_image(pen), cmap="gray")
ax[0,0].set_title("Normalized Pen")

ax[0,1].imshow(to_image(noise), cmap="gray")
ax[0,1].set_title("Normalized Noise")

ax[0,2].imshow(to_image(bundle(pen, noise)), cmap="gray")
ax[0,2].set_title("Bundle(Pen + Noise)")

# Row 2: shoes / noise / bundle(shoes, noise)
ax[1,0].imshow(to_image(shoes), cmap="gray")
ax[1,0].set_title("Normalized Shoes")

ax[1,1].imshow(to_image(noise), cmap="gray")
ax[1,1].set_title("Normalized Noise")

ax[1,2].imshow(to_image(bundle(shoes, noise)), cmap="gray")
ax[1,2].set_title("Bundle(Shoes + Noise)")

# Row 3: pen / shoes / bundle(pen, shoes)
ax[2,0].imshow(to_image(pen), cmap="gray")
ax[2,0].set_title("Normalized Pen")

ax[2,1].imshow(to_image(shoes), cmap="gray")
ax[2,1].set_title("Normalized Shoes")

ax[2,2].imshow(to_image(bundle(pen, shoes)), cmap="gray")
ax[2,2].set_title("Bundle(Pen + Shoes)")

for a in ax.ravel():
  a.axis("off")

plt.tight_layout()
plt.savefig('bundles.jpg')


# ------------------------------------------------------------
# Visualization (FIGURE 2: 3x5 layout with binding + recovery)
# ------------------------------------------------------------

fig2, ax = plt.subplots(3, 5, figsize=(18, 10))

# ---------------- Row 1: Pen + Noise binding ----------------
ax[0,0].imshow(to_image(pen), cmap="gray")
ax[0,0].set_title("Normalized Pen")

ax[0,1].imshow(to_image(noise), cmap="gray")
ax[0,1].set_title("Normalized Noise")

bind_pn = bind(pen, noise)
ax[0,2].imshow(to_image(bind_pn), cmap="gray")
ax[0,2].set_title("Bind(Pen, Noise)")

recover_pen_from_pn = bind(bind_pn, inverse(noise))
ax[0,3].imshow(to_image(recover_pen_from_pn), cmap="gray")
ax[0,3].set_title("Recovered Pen")

recover_noise_from_pn = bind(bind_pn, inverse(pen))
ax[0,4].imshow(to_image(recover_noise_from_pn), cmap="gray")
ax[0,4].set_title("Recovered Noise")


# ---------------- Row 2: Shoes + Noise binding ----------------
ax[1,0].imshow(to_image(shoes), cmap="gray")
ax[1,0].set_title("Normalized Shoes")

ax[1,1].imshow(to_image(noise), cmap="gray")
ax[1,1].set_title("Normalized Noise")

bind_sn = bind(shoes, noise)
ax[1,2].imshow(to_image(bind_sn), cmap="gray")
ax[1,2].set_title("Bind(Shoes, Noise)")

recover_shoes_from_sn = bind(bind_sn, inverse(noise))
ax[1,3].imshow(to_image(recover_shoes_from_sn), cmap="gray")
ax[1,3].set_title("Recovered Shoes")

recover_noise_from_sn = bind(bind_sn, inverse(shoes))
ax[1,4].imshow(to_image(recover_noise_from_sn), cmap="gray")
ax[1,4].set_title("Recovered Noise")


# ---------------- Row 3: Shoes + Pen binding ----------------
ax[2,0].imshow(to_image(shoes), cmap="gray")
ax[2,0].set_title("Normalized Shoes")

ax[2,1].imshow(to_image(pen), cmap="gray")
ax[2,1].set_title("Normalized Pen")

bind_sp = bind(shoes, pen)
ax[2,2].imshow(to_image(bind_sp), cmap="gray")
ax[2,2].set_title("Bind(Shoes, Pen)")

recover_shoes_from_sp = bind(bind_sp, inverse(pen))
ax[2,3].imshow(to_image(recover_shoes_from_sp), cmap="gray")
ax[2,3].set_title("Recovered Shoes")

recover_pen_from_sp = bind(bind_sp, inverse(shoes))
ax[2,4].imshow(to_image(recover_pen_from_sp), cmap="gray")
ax[2,4].set_title("Recovered Pen")


for a in ax.ravel():
  a.axis("off")

plt.tight_layout()
plt.savefig('binds.jpg')


# --------------------------------------------------------------
# Leveling (FIGURE 3)
# --------------------------------------------------------------

LEVELS = 10

fig, ax = plt.subplots(
  3,
  LEVELS,
  figsize=(2 * LEVELS, 6)
)

rows = [
  ("Shoes → Noise", make_levels(LEVELS, shoes, noise), shoes, noise),
  ("Pen → Noise",   make_levels(LEVELS, pen, noise),   pen,   noise),
  ("Pen → Shoes",   make_levels(LEVELS, pen, shoes),   pen,   shoes),
]

for r, (label, levels_dict, start, end) in enumerate(rows):

  for c in range(LEVELS):

    level = levels_dict[c]

    ax[r, c].imshow(to_image(level), cmap="gray")

    ax[r, c].set_xticks([])
    ax[r, c].set_yticks([])
    ax[r, c].set_frame_on(False)

    if r == 0:
      pct = int(round(100 * c / (LEVELS - 1)))
      ax[r, c].set_title(f"{pct}%")

    if c == 0:
      ax[r, c].set_ylabel(label, fontsize=12)

    sim_start = cosine_similarity(level, start)
    sim_end = cosine_similarity(level, end)

    ax[r, c].set_xlabel(
      f"{sim_start:.2f}\n{sim_end:.2f}",
      fontsize=7
    )

plt.subplots_adjust(
  left=0.04,
  right=0.99,
  top=0.90,
  bottom=0.10,
  wspace=0.02,
  hspace=0.18
)

plt.savefig("levels.jpg")



# histograms

# ------------------------------------------------------------
# Histogram helper
# ------------------------------------------------------------

def plot_distribution(ax, data, title):
  ax.hist(
    data.ravel(),
    bins=100,
    range=(-POLE, POLE),
    color="steelblue",
    edgecolor="black",
    alpha=0.8,
  )
  ax.set_title(title)
  ax.set_xlabel("Pixel Value")
  ax.set_ylabel("Count")
  ax.grid(alpha=0.3)


# ------------------------------------------------------------
# Raw vs Stabilized Histograms
# ------------------------------------------------------------

fig, ax = plt.subplots(3, 2, figsize=(10, 10))

pairs = [
    ("Pen", raw_pen, pen),
    ("Shoes", raw_shoes, shoes),
    ("Noise", raw_noise, noise),
]

for r, (name, raw, stable) in enumerate(pairs):

    ax[r, 0].hist(
        raw.ravel(),
        bins=100,
        range=(0, 255),
        color="gray",
        edgecolor="black",
    )
    ax[r, 0].set_title(f"Raw {name}")
    ax[r, 0].set_xlabel("Pixel Value")
    ax[r, 0].set_ylabel("Count")
    ax[r, 0].grid(alpha=0.3)

    ax[r, 1].hist(
        stable.ravel(),
        bins=100,
        range=(-POLE, POLE),
        color="steelblue",
        edgecolor="black",
    )
    ax[r, 1].set_title(f"Stabilized {name}")
    ax[r, 1].set_xlabel("Pixel Value")
    ax[r, 1].set_ylabel("Count")
    ax[r, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("raw_to_stab_hist.jpg", dpi=300)


fig1, ax = plt.subplots(3,3, figsize=(14,12))

plot_distribution(ax[0,0], pen, "Normalized Pen")
plot_distribution(ax[0,1], noise, "Normalized Noise")
plot_distribution(ax[0,2], bundle(pen, noise), "Bundle(Pen + Noise)")

plot_distribution(ax[1,0], shoes, "Normalized Shoes")
plot_distribution(ax[1,1], noise, "Normalized Noise")
plot_distribution(ax[1,2], bundle(shoes, noise), "Bundle(Shoes + Noise)")

plot_distribution(ax[2,0], pen, "Normalized Pen")
plot_distribution(ax[2,1], shoes, "Normalized Shoes")
plot_distribution(ax[2,2], bundle(pen, shoes), "Bundle(Pen + Shoes)")

plt.tight_layout()
plt.savefig("bundles_hist.jpg")


fig2, ax = plt.subplots(3,5, figsize=(18,10))

# Row 1
bind_pn = bind(pen, noise)
recover_pen_from_pn = bind(bind_pn, inverse(noise))
recover_noise_from_pn = bind(bind_pn, inverse(pen))

plot_distribution(ax[0,0], pen, "Normalized Pen")
plot_distribution(ax[0,1], noise, "Normalized Noise")
plot_distribution(ax[0,2], bind_pn, "Bind(Pen, Noise)")
plot_distribution(ax[0,3], recover_pen_from_pn, "Recovered Pen")
plot_distribution(ax[0,4], recover_noise_from_pn, "Recovered Noise")

# Row 2
bind_sn = bind(shoes, noise)
recover_shoes_from_sn = bind(bind_sn, inverse(noise))
recover_noise_from_sn = bind(bind_sn, inverse(shoes))

plot_distribution(ax[1,0], shoes, "Normalized Shoes")
plot_distribution(ax[1,1], noise, "Normalized Noise")
plot_distribution(ax[1,2], bind_sn, "Bind(Shoes, Noise)")
plot_distribution(ax[1,3], recover_shoes_from_sn, "Recovered Shoes")
plot_distribution(ax[1,4], recover_noise_from_sn, "Recovered Noise")

# Row 3
bind_sp = bind(shoes, pen)
recover_shoes_from_sp = bind(bind_sp, inverse(pen))
recover_pen_from_sp = bind(bind_sp, inverse(shoes))

plot_distribution(ax[2,0], shoes, "Normalized Shoes")
plot_distribution(ax[2,1], pen, "Normalized Pen")
plot_distribution(ax[2,2], bind_sp, "Bind(Shoes, Pen)")
plot_distribution(ax[2,3], recover_shoes_from_sp, "Recovered Shoes")
plot_distribution(ax[2,4], recover_pen_from_sp, "Recovered Pen")

plt.tight_layout()
plt.savefig("binds_hist.jpg")



# --------------------------------------------------------------
# Leveling (FIGURE 3: Pixel distributions)
# --------------------------------------------------------------

LEVELS = 10

fig, ax = plt.subplots(
  3,
  LEVELS,
  figsize=(2.2 * LEVELS, 7),
  sharex=True,
  sharey=True,
)

rows = [
  ("Shoes → Noise", make_levels(LEVELS, shoes, noise), shoes, noise),
  ("Pen → Noise",   make_levels(LEVELS, pen, noise),   pen,   noise),
  ("Pen → Shoes",   make_levels(LEVELS, pen, shoes),   pen,   shoes),
]

for r, (label, levels_dict, start, end) in enumerate(rows):

  for c in range(LEVELS):

    level = levels_dict[c]

    ax[r, c].hist(
      level.ravel(),
      bins=100,
      range=(-POLE, POLE),
      color="steelblue",
      edgecolor="black",
      linewidth=0.25,
    )

    if r == 0:
      pct = int(round(100 * c / (LEVELS - 1)))
      ax[r, c].set_title(f"{pct}%")

    if c == 0:
      ax[r, c].set_ylabel(label)

    sim_start = cosine_similarity(level, start)
    sim_end = cosine_similarity(level, end)

    ax[r, c].set_xlabel(
      f"{sim_start:.2f}\n{sim_end:.2f}",
      fontsize=7,
    )

    ax[r, c].grid(alpha=0.25)

plt.tight_layout()
plt.savefig("levels_hist.jpg")
