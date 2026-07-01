import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from scipy.ndimage import gaussian_filter
from PIL import Image


# --------------------------------------------------------
# Utility Functions
# --------------------------------------------------------

def load_image(filename):
    img = Image.open(filename).convert('L')
    img = np.array(img, dtype=np.float64)

    h, w = img.shape
    N = min(h, w)
    img = img[:N, :N]

    return img


def rotational_average(power):

    N = power.shape[0]

    y, x = np.indices((N, N))
    center = N // 2

    r = np.sqrt((x-center)**2 + (y-center)**2).astype(np.int32)

    tbin = np.bincount(r.ravel(), power.ravel())
    nr = np.bincount(r.ravel())

    profile = tbin / nr

    return profile[:N//2+1]


def power_spectrum(im):

    N = im.shape[0]

    imf = np.fft.fftshift(np.fft.fft2(im))
    power = np.abs(imf)**2

    return imf, power


# --------------------------------------------------------
# Figure 1
# Images + Power Spectra + Rotational Average
# --------------------------------------------------------

images = ["../images/shoes.jpg",
          "../images/pen.jpg",
          "../images/noise.jpg"]

fig, axes = plt.subplots(3, 3, figsize=(14,12))

for row, file in enumerate(images):

    im = load_image(file)
    N = im.shape[0]

    imf, power = power_spectrum(im)

    f = np.arange(-N//2, N//2)

    Pf = rotational_average(power)

    axes[row,0].imshow(im,cmap='gray')
    axes[row,0].set_title(file)
    axes[row,0].axis('off')

    axes[row,1].imshow(np.log10(power+1),
                       cmap='viridis',
                       extent=[f[0],f[-1],f[0],f[-1]],
                       origin='lower')
    axes[row,1].set_title("Log Power Spectrum")

    axes[row,2].loglog(Pf[1:])
    axes[row,2].grid(True)
    axes[row,2].set_title("Rotational Average")
    axes[row,2].set_xlabel("Frequency")
    axes[row,2].set_ylabel("Power")

plt.tight_layout()



# --------------------------------------------------------
# Whitening
# --------------------------------------------------------

img = load_image("../images/shoes.jpg")
N = img.shape[0]

imf, power = power_spectrum(img)

f = np.arange(-N//2, N//2)

fx, fy = np.meshgrid(f, f)

rho = np.sqrt(fx**2 + fy**2)

filtf = rho*np.exp(-0.5*(rho/(0.7*N/2))**2)

imwf = filtf*imf

imw = np.real(np.fft.ifft2(np.fft.ifftshift(imwf)))



# --------------------------------------------------------
# Contrast Normalization
# --------------------------------------------------------

D = 16

local_var = gaussian_filter(imw**2,
                            sigma=D/2)

imn = imw/np.sqrt(local_var+1e-8)



# --------------------------------------------------------
# Figure 2
# Whitening Results
# --------------------------------------------------------

fig, ax = plt.subplots(1,4,figsize=(18,5))

ax[0].imshow(filtf,cmap='viridis')
ax[0].set_title("Whitening Filter")
ax[0].axis('off')

ax[1].imshow(imw,cmap='gray')
ax[1].set_title("Whitened Image")
ax[1].axis('off')

ax[2].imshow(imn,cmap='gray')
ax[2].set_title("Contrast Normalized")
ax[2].axis('off')

Pwf = rotational_average(np.abs(imwf)**2)

ax[3].loglog(Pwf[1:])
ax[3].grid(True)
ax[3].set_title("Whitened Spectrum")

plt.tight_layout()



# --------------------------------------------------------
# Random Receptive Field
# --------------------------------------------------------

w = np.random.randn(D,D)

w -= np.mean(w)
w /= np.sqrt(np.sum(w**2))

response = convolve2d(imn,
                      w,
                      mode='same')

mu = response.mean()
sigma = response.std()

hist, bins = np.histogram(response,
                          bins=250,
                          density=True)

centers = (bins[:-1]+bins[1:])/2

gaussian = (1/(sigma*np.sqrt(2*np.pi))
            *np.exp(-(centers-mu)**2/(2*sigma**2)))



# --------------------------------------------------------
# Figure 3
# Random RF
# --------------------------------------------------------

fig, ax = plt.subplots(1,2,figsize=(12,5))

ax[0].imshow(w,cmap='gray')
ax[0].set_title("Random Receptive Field")

ax[1].semilogy(centers,
               hist,
               label="Response")

ax[1].semilogy(centers,
               gaussian,
               'k--',
               label="Gaussian")

ax[1].legend()
ax[1].set_title("Random RF Histogram")
ax[1].set_xlabel("Response")
ax[1].set_ylabel("Probability")

plt.tight_layout()



# --------------------------------------------------------
# Gabor Filter
# --------------------------------------------------------

x = np.arange(-D//2,D//2)
y = np.arange(-D//2,D//2)

X,Y = np.meshgrid(x,y)

sigma_x = 2
sigma_y = 2
fx = 0.25

g = np.exp(
        -0.5*((X/sigma_x)**2 +
              (Y/sigma_y)**2)
    ) * np.sin(2*np.pi*fx*X)

g /= np.sqrt(np.sum(g**2))

response = convolve2d(imn,
                      g,
                      mode='same')

mu = response.mean()
sigma = response.std()

hist,bins = np.histogram(response,
                         bins=250,
                         density=True)

centers = (bins[:-1]+bins[1:])/2

gaussian = (1/(sigma*np.sqrt(2*np.pi))
            *np.exp(-(centers-mu)**2/(2*sigma**2)))



# --------------------------------------------------------
# Figure 4
# Sparse Gabor
# --------------------------------------------------------

fig, ax = plt.subplots(1,2,figsize=(12,5))

ax[0].imshow(g,cmap='gray')
ax[0].set_title("Sparse Gabor")

ax[1].semilogy(centers,
               hist,
               label="Response")

ax[1].semilogy(centers,
               gaussian,
               'k--',
               label="Gaussian")

ax[1].legend()
ax[1].set_title("Sparse Histogram")
ax[1].set_xlabel("Response")

plt.tight_layout()



# --------------------------------------------------------
# Least Sparse Gabor
# --------------------------------------------------------

sigma_x = 8
sigma_y = 8
fx = 0.05

g2 = np.exp(
        -0.5*((X/sigma_x)**2 +
              (Y/sigma_y)**2)
    ) * np.sin(2*np.pi*fx*X)

g2 /= np.sqrt(np.sum(g2**2))

response = convolve2d(imn,
                      g2,
                      mode='same')

mu = response.mean()
sigma = response.std()

hist,bins = np.histogram(response,
                         bins=250,
                         density=True)

centers = (bins[:-1]+bins[1:])/2

gaussian = (1/(sigma*np.sqrt(2*np.pi))
            *np.exp(-(centers-mu)**2/(2*sigma**2)))



# --------------------------------------------------------
# Figure 5
# Least Sparse Gabor
# --------------------------------------------------------

fig, ax = plt.subplots(1,2,figsize=(12,5))

ax[0].imshow(g2,cmap='gray')
ax[0].set_title("Least Sparse Gabor")

ax[1].semilogy(centers,
               hist,
               label="Response")

ax[1].semilogy(centers,
               gaussian,
               'k--',
               label="Gaussian")

ax[1].legend()
ax[1].set_title("Least Sparse Histogram")
ax[1].set_xlabel("Response")

plt.tight_layout()

plt.show()
