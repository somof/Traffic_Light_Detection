# import keras
# from keras.preprocessing import image
# import tkinter

from scipy.misc import imread

import pickle

import matplotlib
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt

# from tl_classifier import TLClassifier

#gt = pickle.load(open('TLD201803-3-capture.p', 'rb'))
with open('TLD201803-3-capture-2.p', 'rb') as f:
    u = pickle._Unpickler(f)
    u.encoding = 'latin1'
    gt = u.load()
keys = sorted(gt.keys())
print(len(keys))

tld_classes = ['RED', 'YELLOW', 'GREEN', 'unknown']
tld_color = ['red', 'yellow', 'green', 'grey']
path_prefix = 'images.capture/'


if __name__ == '__main__':
    # light_classifier = TLClassifier()

    #fig, ax = plt.subplots(1, 1)
    # plt.ion()
    ax = plt.subplot()
    # plt.figure(1).show()

    for key in keys:
        img_path = path_prefix + key
        rect = gt[key]
        label = 4
        if rect[0][4] != 0:
            label = 0
        elif rect[0][5] != 0:
            label = 1
        elif rect[0][6] != 0:
            label = 2

        # if label != 0:
        #     continue

        # print(img_path, rect)

        # img = image.load_img(img_path)
        img = imread(img_path)
    

        xmin = int(rect[0][0] * img.shape[1])
        ymin = int(rect[0][1] * img.shape[0])
        xmax = int(rect[0][2] * img.shape[1])
        ymax = int(rect[0][3] * img.shape[0])
        # height = ymax - ymin
        # width = height * 0.4
        # xmin = int(xmax - width)
        # xmin -= 5
        # xmax += 5
        # ymin -= 5
        # ymax += 5

        # if 790 < xmax:
        #     continue

        # xmin = float(rect[0][0])
        # ymin = float(rect[0][1])
        # xmax = float(rect[0][2])
        # ymax = float(rect[0][3])
        # height = ymax - ymin
        # width = height * 0.37
        # xmin = xmax - width
        # xmin -= 0.05 * width
        # xmax += 0.05 * height
        # ymin -= 0.05 * width
        # ymax += 0.05 * height
        # xmin = int(xmin * img.shape[1])
        # ymin = int(ymin * img.shape[0])
        # xmax = int(xmax * img.shape[1])
        # ymax = int(ymax * img.shape[0])

        # exit(0)


        if 0 <= label < 4:
            ax.cla()
            plt.imshow(img / 255.)
            currentAxis = plt.gca()

            coords = (xmin, ymin), xmax - xmin + 1, ymax - ymin + 1
            display_txt = '{}:{}'.format(label, tld_classes[label])
            color = tld_color[label]
            currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
            currentAxis.text(xmin, ymin, display_txt, bbox={'facecolor':color, 'alpha':0.5})

            print(label, xmin, xmax, ymin, ymax, img_path)

            #plt.show()
            plt.draw()
            plt.pause(0.1)
