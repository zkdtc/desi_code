import os
import desispec.preproc as preproc
import numpy as np
import matplotlib.pyplot as plt
img=preproc.read_bias_plus_dark(filename='master_bias_dark_z9.fits',exptime=830)

n = 8
img1 = np.zeros((n, n))
img2 = np.zeros((n, n))

img1[2:4, 2:4] = 1
img2[4:6, 4:6] = 1

plt.figure()
plt.imshow(img1)

plt.figure()
plt.imshow(img2)

img3=preproc.interp_two_images(img1, img2, 0.1)
plt.figure()
plt.imshow(img3)
plt.colorbar()

plt.show()

