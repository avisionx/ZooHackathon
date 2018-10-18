import cv2
import numpy as np
import scipy
from scipy.misc import imread
import pickle
import random
import os
import matplotlib.pyplot as plt
import argparse    
import cv2

parser = argparse.ArgumentParser()

parser.add_argument("--file", dest='myfile')
args = parser.parse_args()
s = args.myfile

# Feature extractor
def extract_features(image_path, vector_size=32):
    image = imread(image_path, mode ="RGB")
    
    # gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # mask = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    # # mask = cv2.bitwise_not(mask)
    # image = cv2.bitwise_and(image,image, mask= mask)  
    # plt.imshow(image)
    # plt.show()

    # grey = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    # grey = clahe.apply(grey)
    # blur = cv2.GaussianBlur(grey,(5,5),0)
    # _,mask = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # image = mask

    # rows, cols, dep = image.shape
    # lower = np.array([0,0,0])

    # upper = np.array([255,255,100])

    # hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    # mask = cv2.inRange(hsv, lower, upper)
    # res = cv2.bitwise_and(image,image, mask= mask)
    # image = cv2.bitwise_not(mask)


    # plt.imshow(mask)
    # plt.show()

    try:
        # Using KAZE, cause SIFT, ORB and other was moved to additional module
        # which is adding addtional pain during install
        print("ORB create")
        alg = cv2.ORB_create()
        # Dinding image keypoints
        print("ORB detect")
        kps = alg.detect(image)
        # Getting first 32 of them. 
        # Number of keypoints is varies depend on image size and color pallet
        # Sorting them based on keypoint response value(bigger is better)
        kps = sorted(kps, key=lambda x: -x.response)[:vector_size]
        # computing descriptors vector
        print("ORB compute")
        kps, dsc = alg.compute(image, kps)
        # Flatten all of them in one big vector - our feature vector
        dsc = dsc.flatten()
        # Making descriptor of same size
        # Descriptor vector size is 64
        needed_size = (vector_size * 64)
        if dsc.size < needed_size:
            # if we have less the 32 descriptors then just adding zeros at the
            # end of our feature vector
            dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
    except cv2.error as e:
        print ('Error: ', e)
        return None

    return dsc


def batch_extractor(images_path, pickled_db_path="features.pck"):
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]

    result = {}
    for f in files:
        print ('Extracting features from image %s' % f)
        name = f.split('/')[-1].lower()
        result[name] = extract_features(f)
    
    # saving all our feature vectors in pickled file
    with open(pickled_db_path, 'wb') as fp:
        pickle.dump(result, fp)

class Matcher(object):

    def __init__(self, pickled_db_path="features.pck"):
        with open(pickled_db_path, 'rb') as fp:
            self.data = pickle.load(fp)
        self.names = []
        self.matrix = []
        for k, v in self.data.items():
            self.names.append(k)
            self.matrix.append(v)
        self.matrix = np.array(self.matrix)
        self.names = np.array(self.names)

    def cos_cdist(self, vector):
        # getting cosine distance between search image and images database
        v = vector.reshape(1, -1)
        return scipy.spatial.distance.cdist(self.matrix, v, 'cosine').reshape(-1)

    def match(self, image_path, topn=5):
        features = extract_features(image_path)
        print("Features extracted")
        img_distances = self.cos_cdist(features)

        # getting top 5 records
        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()

        return nearest_img_paths, img_distances[nearest_ids].tolist()

def show_img(path):
    path = './media/' + path
    img = imread(path, mode="RGB")
    plt.imshow(img)
    plt.show()
    
def run():
    images_path = './media/animals/'
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    # getting 3 random images 
    # sample = random.sample(files, 5)
    sample = files
    batch_extractor(images_path)

    ma = Matcher('features.pck')
    
    print ('Query image ==========================================')
    show_img(s)
    names, match = ma.match('./media/' + s, topn=5)
    print ('Result images ========================================')
    for i in range(3):
        # we got cosine distance, less cosine distance between vectors
        # more they similar, thus we subtruct it from 1 to get match value
        print ('Match %s' % (1-match[i]))
        show_img('./animals/'+ names[i])
run()