import pickle

from keras.preprocessing import image
from scipy.misc import imread

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#from tl_classifier import TLClassifier

with open('TLD20180320-3-supp.p', 'rb') as f:
    u = pickle._Unpickler(f)
    u.encoding = 'latin1'
    gt = u.load()
keys = sorted(gt.keys())

tld_classes = ['RED', 'YELLOW', 'GREEN', 'unknown']
tld_color = ['red', 'yellow', 'green', 'grey']


if __name__ == '__main__':

    #fig, ax = plt.subplots(1, 1)
#    plt.ion()
    fig, ax = plt.subplots()

    for img_basename in keys:

        inputs = []
        images = []
        #img_basename = 'frame000{:03d}.png'.format(i)
#        img_path = 'parkinglot/' + img_basename
        img_path = 'images/' + img_basename
        img = image.load_img(img_path)
        img = image.img_to_array(img) # to 3D numpy.array

        ax.cla()
        plt.imshow(img / 255.)
        currentAxis = plt.gca()

        try:
            rect = gt[img_basename]
            print(img_basename)
            #print(rect)
            label = 4
            if rect[0][4]:
                label = 0
            elif rect[0][5]:
                label = 1
            elif rect[0][6]:
                label = 2

            if label != 4:
                top_xmin = rect[0][0]
                top_ymin = rect[0][1]
                top_xmax = rect[0][2]
                top_ymax = rect[0][3]
                xmin = int(round(top_xmin * img.shape[1]))
                ymin = int(round(top_ymin * img.shape[0]))
                xmax = int(round(top_xmax * img.shape[1]))
                ymax = int(round(top_ymax * img.shape[0]))

                coords = (xmin, ymin), xmax - xmin + 1, ymax - ymin + 1
                color = tld_color[label]
                currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=1))
        except:
            pass

#        plt.show()
        plt.pause(0.01)

#        anim = ArtistAnimation(fig, artists, interval=1000)
