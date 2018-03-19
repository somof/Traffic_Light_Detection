#import cv2
import keras
from keras.applications.imagenet_utils import preprocess_input
#from keras.backend.tensorflow_backend import set_session
#from keras.models import Model
from keras.preprocessing import image
import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import pickle
#from random import shuffle
from scipy.misc import imread
from scipy.misc import imresize
import tensorflow as tf

from ssd import SSD300
from ssd_training import MultiboxLoss
from ssd_utils import BBoxUtility

np.set_printoptions(suppress=True)

# some constants
NUM_CLASSES = 3 + 1
input_shape = (300, 300, 3)

# "prior boxes" in the paper
priors = pickle.load(open('prior_boxes_ssd300.pkl', 'rb'))
bbox_util = BBoxUtility(NUM_CLASSES, priors)

model = SSD300(input_shape, num_classes=NUM_CLASSES)
model.load_weights('checkpoints/weights.99-0.70.hdf5', by_name=True)
#model.load_weights('weights.05.hdf5', by_name=True)




inputs = []
images = []
#img_path = 'images/frame000000.png'
#img = image.load_img(img_path, target_size=(300, 300))
#img = image.img_to_array(img)
#images.append(imread(img_path))
#inputs.append(img.copy())
#img_path = 'images/frame000010.png'
#img = image.load_img(img_path, target_size=(300, 300))
#img = image.img_to_array(img)
#images.append(imread(img_path))
#inputs.append(img.copy())
#img_path = 'images/frame000020.png'
#img = image.load_img(img_path, target_size=(300, 300))
#img = image.img_to_array(img)
#images.append(imread(img_path))
#inputs.append(img.copy())
#img_path = 'images/frame000100.png'
#img = image.load_img(img_path, target_size=(300, 300))
#img = image.img_to_array(img)
#images.append(imread(img_path))
#inputs.append(img.copy())
#img_path = 'images/frame000300.png'
#img = image.load_img(img_path, target_size=(300, 300))
#img = image.img_to_array(img)
#images.append(imread(img_path))
#inputs.append(img.copy())

for i in range(0, 710, 10):
    img_path = 'images/frame000{:03d}.png'.format(i)
    #print(img_path)
    img = image.load_img(img_path)  # , target_size=(300, 300))
    #print(np.array(img).shape)
    img = imresize(img, (300, 300))
    img = image.img_to_array(img)
    images.append(imread(img_path))
    inputs.append(img.copy())

print(np.array(inputs).shape)

inputs = preprocess_input(np.array(inputs))
preds = model.predict(inputs, batch_size=1, verbose=1)
results = bbox_util.detection_out(preds)


#%matplotlib inline
plt.rcParams['figure.figsize'] = (8, 8)
plt.rcParams['image.interpolation'] = 'nearest'

tld_classes = ['RED', 'YELLOW', 'GREEN', 'unknown']
tld_color = ['red', 'yellow', 'green', 'grey']

for j, img in enumerate(images):
    # Parse the outputs.
    det_label = results[j][:, 0]
    det_conf = results[j][:, 1]
    det_xmin = results[j][:, 2]
    det_ymin = results[j][:, 3]
    det_xmax = results[j][:, 4]
    det_ymax = results[j][:, 5]

    # Get detections with confidence
    top_indices = [j for j, conf in enumerate(det_conf) if conf >= 0.8]

    top_conf = det_conf[top_indices]
    top_label_indices = det_label[top_indices].tolist()
    top_xmin = det_xmin[top_indices]
    top_ymin = det_ymin[top_indices]
    top_xmax = det_xmax[top_indices]
    top_ymax = det_ymax[top_indices]

    plt.imshow(img / 255.)
    currentAxis = plt.gca()

    for i in range(top_conf.shape[0]):
        xmin = int(round(top_xmin[i] * img.shape[1]))
        ymin = int(round(top_ymin[i] * img.shape[0]))
        xmax = int(round(top_xmax[i] * img.shape[1]))
        ymax = int(round(top_ymax[i] * img.shape[0]))
        score = top_conf[i]
        label = int(top_label_indices[i])
        display_txt = '{:0.2f}, {}:{}'.format(score, label - 1, tld_classes[label - 1])
        print(j, i, display_txt)
        coords = (xmin, ymin), xmax-xmin+1, ymax-ymin+1
        color = tld_color[label - 1]
        currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
        currentAxis.text(xmin, ymin, display_txt, bbox={'facecolor':color, 'alpha':0.5})
    plt.show()
