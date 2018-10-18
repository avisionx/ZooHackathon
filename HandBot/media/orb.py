import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import os

def image_detect_and_compute(detector, img_name):
	"""Detect and compute interest points and their descriptors."""
	img = cv2.imread(os.path.join(dataset_path, img_name))
	
	# lower = np.array([0,0,0])
	# upper = np.array([255,255,100])
	# hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	# mask = cv2.inRange(hsv, lower, upper)
	# res = cv2.bitwise_and(img,img, mask= mask)
	# image = cv2.bitwise_not(mask)
	
	# grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	# clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
	# grey = clahe.apply(grey)
	# blur = cv2.GaussianBlur(grey,(5,5),0)
	# _,mask = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	# image = mask

	# plt.imshow(image,cmap='Greys_r')
	# plt.show()
	img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
	kp, des = detector.detectAndCompute(img, None)
	return img, kp, des
	

def draw_image_matches(detector, img1_name, img2_name, nmatches=10):
	"""Draw ORB feature matches of the given two images."""
	img1, kp1, des1 = image_detect_and_compute(detector, img1_name)
	img2, kp2, des2 = image_detect_and_compute(detector, img2_name)
	
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
	matches = bf.match(des1, des2)
	matches = sorted(matches, key = lambda x: x.distance) # Sort matches by distance.  Best come first.
	
	img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches[:nmatches], img2, flags=2) # Show top 10 matches
	plt.figure(figsize=(16, 16))
	plt.title(type(detector))
	plt.imshow(img_matches); plt.show()

def draw_image_matches2(detector, img1_name, img2_name, nmatches=30):
	"""Draw ORB feature matches of the given two images."""
	img1, kp1, des1 = image_detect_and_compute(detector, img1_name)
	img2, kp2, des2 = image_detect_and_compute(detector, img2_name)
	
	FLANN_INDEX_KDTREE = 1
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks=50)

	bf = cv2.BFMatcher()
	matches = bf.knnMatch(np.asarray(des1,np.float32), np.asarray(des2,np.float32), k=2)

	matchesMask = [[0, 0] for i in range(len(matches))]
	# ratio test as per Lowe's paper
	for i, (m, n) in enumerate(matches):
		if m.distance < 0.7*n.distance:
			matchesMask[i] = [1, 0]

	draw_params = dict(matchColor=(0, 255, 0),
					   singlePointColor=(255, 0, 0),
					   matchesMask=matchesMask,
					   flags=0)

	img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)
	plt.figure(figsize=(18, 18))
	plt.imshow(img3); plt.show()
	
