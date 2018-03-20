import pickle

import keras
from keras.preprocessing import image
from scipy.misc import imread

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from tl_classifier import TLClassifier

with open('TLD20180319-3-site.p', 'rb') as f:
    u = pickle._Unpickler(f)
    u.encoding = 'latin1'
    gt = u.load()
keys = sorted(gt.keys())

tld_classes = ['RED', 'YELLOW', 'GREEN', 'unknown']
tld_color = ['red', 'yellow', 'green', 'grey']


if __name__ == '__main__':
    light_classifier = TLClassifier()

    count = 0
    #fig, ax = plt.subplots(1, 1)
#    plt.ion()
    fig, ax = plt.subplots()
    testlist = sorted(set.union(set(range(270, 410, 2)), set(range(650, 740,2)), set(range(1005, 1085, 2))))
    #for i in testlist:
    #for i in range(250, 1150, 5):
    for i in range(250, 1150):
    #for i in range(50, 710, 2):
        inputs = []
        images = []
        img_basename = 'frame{:06d}.png'.format(i)
        img_path = 'parkinglot/' + img_basename
        #img_path = 'images/' + img_basename
        img = image.load_img(img_path)
        img = image.img_to_array(img) # to 3D numpy.array

        print(img_basename)


        ax.cla()
        plt.imshow(img / 255.)
        currentAxis = plt.gca()

        #try:
        #    rect = gt[img_basename]
        #    #print(rect)
        #    label = 4
        #    if rect[0][4]:
        #        label = 0
        #    elif rect[0][5]:
        #        label = 1
        #    elif rect[0][6]:
        #        label = 2

        #    if label != 4:
        #        top_xmin = rect[0][0]
        #        top_ymin = rect[0][1]
        #        top_xmax = rect[0][2]
        #        top_ymax = rect[0][3]
        #        xmin = int(round(top_xmin * img.shape[1]))
        #        ymin = int(round(top_ymin * img.shape[0]))
        #        xmax = int(round(top_xmax * img.shape[1]))
        #        ymax = int(round(top_ymax * img.shape[0]))

        #        coords = (xmin, ymin), xmax - xmin + 1, ymax - ymin + 1
        #        color = tld_color[label]
        #        currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=1))
        #except:
        #    pass



        #print(img.shape)
        ## test (1096, 1368, 3)
        ## impl (1096, 1368, 3)

        label, score, top_xmin, top_ymin, top_xmax, top_ymax = light_classifier.get_classification(img)
        #label, score, top_xmin, top_ymin, top_xmax, top_ymax = 4, 0, 0, 0, 0, 0
    
        #display_txt = '{:0.2f}, {}'.format(score, label)
        #print(label, display_txt)

    
        xmin = int(round(top_xmin * img.shape[1]))
        ymin = int(round(top_ymin * img.shape[0]))
        xmax = int(round(top_xmax * img.shape[1]))
        ymax = int(round(top_ymax * img.shape[0]))

        if label != 4:
            coords = (xmin, ymin), xmax - xmin + 1, ymax - ymin + 1
            display_txt = '{:0.2f}, {}:{}'.format(score, label, tld_classes[label])
            color = tld_color[label]
            currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
            currentAxis.text(xmin, ymin, display_txt, bbox={'facecolor':color, 'alpha':0.5})
            #plt.draw()

#        plt.show()
        plt.savefig('predict/res{:06d}.png'.format(count))
        count = count + 1
        plt.pause(0.01)

#        anim = ArtistAnimation(fig, artists, interval=1000)
