import numpy as np
import matplotlib.pyplot as plt
import cv2

from skimage import data, img_as_float
from skimage.measure import compare_ssim as ssim


# img = img_as_float(data.camera())
img = cv2.imread('base.png')
rows, cols, dep = img.shape

img_noise = cv2.imread('same.png')
rows, cols, dep = img_noise.shape

img_const = cv2.imread('duplicate.png')
rows, cols, dep = img_const.shape

# noise = np.ones_like(img) * 0.2 * (img.max() - img.min())
# noise[np.random.random(size=noise.shape) > 0.5] *= -1

img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

img = cv2.cvtColor(img_noise,cv2.COLOR_BGR2GRAY)

ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
img_noise = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

img = cv2.cvtColor(img_const,cv2.COLOR_BGR2GRAY)

ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
img_const = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

# lower = np.array([0,0,0])
# upper = np.array([255,255,100])

# hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
# mask = cv2.inRange(hsv, lower, upper)
# res = cv2.bitwise_and(img,img, mask= mask)
# img = cv2.bitwise_not(mask)

# # cv2.imshow('frame',img)
# # cv2.imshow('mask',mask)
# # cv2.imshow('res',res)
# # cv2.imshow('original',img)
# # cv2.imshow('threshold',threshold)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()

# hsv = cv2.cvtColor(img_noise,cv2.COLOR_BGR2HSV)
# mask = cv2.inRange(hsv, lower, upper)
# res = cv2.bitwise_and(img_noise,img_noise, mask= mask)
# img_noise = cv2.bitwise_not(mask)

# hsv = cv2.cvtColor(img_const,cv2.COLOR_BGR2HSV)
# mask = cv2.inRange(hsv, lower, upper)
# res = cv2.bitwise_and(img_const,img_const, mask= mask)
# img_const = cv2.bitwise_not(mask)

# cv2.imshow('base',img)
# cv2.imshow('same',img_noise)
# cv2.imshow('duplicate',img_const)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


def mse(x, y):
    return np.linalg.norm(x - y)
dim = (500,500)

img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
img_noise = cv2.resize(img_noise, dim, interpolation = cv2.INTER_AREA)
img_const = cv2.resize(img_const, dim, interpolation = cv2.INTER_AREA)

img = img_as_float(img)
img_noise = img_as_float(img_noise)
img_const = img_as_float(img_const)


fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 4),sharex=True, sharey=True)
ax = axes.ravel()

mse_none = mse(img, img)
ssim_none = ssim(img, img, data_range=img.max() - img.min())

mse_noise = mse(img, img_noise)
ssim_noise = ssim(img, img_noise,data_range=img_noise.max() - img_noise.min())

mse_const = mse(img, img_const)
ssim_const = ssim(img, img_const,data_range=img_const.max() - img_const.min())

label = 'MSE: {:.2f}, SSIM: {:.2f}'

ax[0].imshow(img, cmap=plt.cm.gray, vmin=0, vmax=1)
ax[0].set_xlabel(label.format(mse_none, ssim_none))
ax[0].set_title('Original image')

ax[1].imshow(img_noise, cmap=plt.cm.gray, vmin=0, vmax=1)
ax[1].set_xlabel(label.format(mse_noise, ssim_noise))
ax[1].set_title('Same')

ax[2].imshow(img_const, cmap=plt.cm.gray, vmin=0, vmax=1)
ax[2].set_xlabel(label.format(mse_const, ssim_const))
ax[2].set_title('Duplicate')

plt.tight_layout()
plt.show()