import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.ndimage import gaussian_filter, zoom


# ============================================================
# Load Image
# ============================================================

im = Image.open("../images/pen.jpg").convert("L")
im = np.array(im, dtype=np.float32)


plt.figure(figsize=(6, 6))
plt.imshow(im, cmap="gray")
plt.axis("off")
plt.title("Original Image")


# ============================================================
# Laplacian Pyramid Functions
# ============================================================

def buildpyr(im, levels):

    pyr = []
    current = im

    for i in range(levels - 1):

        # Low-pass filter
        smooth = gaussian_filter(current, sigma=1)

        # Downsample
        small = smooth[::2, ::2]

        # Expand back to current size
        expanded = zoom(small, 2, order=1)

        expanded = expanded[:current.shape[0],
                            :current.shape[1]]

        # Laplacian detail layer
        lap = current - expanded

        pyr.append(lap)

        current = small

    # Add top Gaussian level
    pyr.append(current)

    # Top of pyramid first
    pyr.reverse()

    return pyr



def showpyr(pyr, title="Pyramid"):

    plt.figure(figsize=(16, 4))

    for i, level in enumerate(pyr):

        h, w = level.shape

        plt.subplot(1, len(pyr), i + 1)

        plt.imshow(level, cmap="gray")
        plt.axis("off")

        plt.title(
            f"{w}x{h}\nLevel {i}"
        )

    plt.suptitle(title)



def reconpyr(pyr):

    image = pyr[0]

    for level in pyr[1:]:

        expanded = zoom(
            image,
            2,
            order=1
        )

        expanded = expanded[:level.shape[0],
                            :level.shape[1]]

        image = expanded + level

    return image



# ============================================================
# Build and Display Pyramid
# ============================================================

pyr = buildpyr(im, 4)

showpyr(
    pyr,
    "4-Level Laplacian Pyramid"
)



# ============================================================
# Reconstruction
# ============================================================

imh = reconpyr(pyr)


plt.figure(figsize=(6, 6))
plt.imshow(imh, cmap="gray")
plt.axis("off")
plt.title("Reconstructed Image")



# ============================================================
# Window Pyramid
# ============================================================

def windowpyr(pyr, radius=16):

    pyrw = []

    for level in pyr:

        h, w = level.shape

        y, x = np.mgrid[
            0:h,
            0:w
        ]

        cx = w / 2
        cy = h / 2

        distance = np.sqrt(
            (x - cx)**2 +
            (y - cy)**2
        )

        # Gaussian window
        window = np.exp(
            -(distance**2) /
            (2 * radius**2)
        )

        pyrw.append(
            level * window
        )

    return pyrw



# ============================================================
# Default Retina Simulation (32 pixel window)
# ============================================================

pyrw = windowpyr(
    pyr,
    radius=16
)

showpyr(
    pyrw,
    "Windowed Pyramid (Radius = 16)"
)


imh_window = reconpyr(pyrw)


plt.figure(figsize=(6, 6))
plt.imshow(
    imh_window,
    cmap="gray"
)

plt.axis("off")
plt.title(
    "Windowed Reconstruction"
)



# ============================================================
# Parvocellular Simulation
# D = 0.01r
# Window diameter = 200
# Radius = 100
# ============================================================

pyr_parvo = windowpyr(
    pyr,
    radius=100
)


showpyr(
    pyr_parvo,
    "Parvocellular Windowed Pyramid"
)


imh_parvo = reconpyr(
    pyr_parvo
)


plt.figure(figsize=(6, 6))

plt.imshow(
    imh_parvo,
    cmap="gray"
)

plt.axis("off")

plt.title(
    "Parvocellular Lattice"
)






# ============================================================
# Magnocellular Simulation
# Larger dendritic fields
# Window diameter = 100
# Radius = 50
# ============================================================

pyr_magno = windowpyr(
    pyr,
    radius=50
)


showpyr(
    pyr_magno,
    "Magnocellular Windowed Pyramid"
)


imh_magno = reconpyr(
    pyr_magno
)


plt.figure(figsize=(6, 6))

plt.imshow(
    imh_magno,
    cmap="gray"
)

plt.axis("off")

plt.title(
    "Magnocellular Lattice"
)



plt.show()
