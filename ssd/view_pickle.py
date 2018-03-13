"""
    with open('VOC2007.pkl2', 'rb') as f:
{u'006688.jpg': array([[ 0.136     ,  0.13903743,  1.        ,  0.77005348,  0.        ,
         0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
         0.        ,  1.        ,  0.        ,  0.        ,  0.        ,
         0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
         0.        ,  0.        ,  0.        ,  0.        ],
       [ 0.196     ,  0.59625668,  1.        ,  1.        ,  0.        ,
         0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
         0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
         0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
         0.        ,  0.        ,  0.        ,  1.        ]]), u'002100.jpg': array([[ 0.468     ,  0.62133333,  0.532     ,  0.75733333,  0.        ,
         0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
         0.        ,  0.        ,  1.        ,  0.        ,  0.        ,
         0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
         0.        ,  0.        ,  0.        ,  0.        ],
       [ 0.338     ,  0.62666667,  0.42      ,  0.75733333,  0.        ,
         0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
         0.        ,  0.        ,  1.        ,  0.        ,  0.        ,
         0.        ,  0.        ,  0.        ,  0.        ,  0.        ,

with open('TLD201803-4.p', 'rb') as f:

{'frame000609.png': array([[0.18201754, 0.31113139, 0.05994152, 0.19890511, 0., 0., 1., 0.]]),
 'frame000682.png': array([[0.17909357, 0.31569343, 0.06359649, 0.17518248, 0., 0., 1., 0.]]),
 'frame000056.png': array([[0.46345029, 0.37317518, 0.02339181, 0.07025547, 0., 0., 1., 0.]]),
 'frame000555.png': array([[0.3874269 , 0.3330292 , 0.04751462, 0.13777372, 1., 0., 0., 0.]]),
 'frame000419.png': array([[0.4627193 , 0.36770073, 0.03143275, 0.08576642, 0., 1., 0., 0.]]),
 'frame000588.png': array([[0.18932749, 0.30474453, 0.06578947, 0.18521898, 0., 0., 1., 0.]]),


with open('prior_boxes_ssd300.pkl', 'rb') as f:
(7308, 8)
[[0.         0.         0.06315789 ... 0.1        0.2        0.2       ]
 [0.         0.         0.08386857 ... 0.1        0.2        0.2       ]
 [0.         0.         0.04851323 ... 0.1        0.2        0.2       ]
 ...
 [0.17473088 0.         0.8252691  ... 0.1        0.2        0.2       ]
 [0.         0.23441887 1.         ... 0.1        0.2        0.2       ]
 [0.23441887 0.         0.76558113 ... 0.1        0.2        0.2       ]]

Hello @KevinYuk,

the file prior_boxes_ssd300.pkl contains 7308 bounding boxes. 
Every box contains x_min, y_min, x_max, y_max, variance_1, variance_2, variance_3, variance_4. 
This bounding boxes are referred in the paper as prior boxes. 
All boxes dimensions are normalized and should have a similar aspects as the ones depcited in the next figure



"""

import numpy as np
import pickle

if __name__ == '__main__':

    # load pickle data set annotation
    #with open('VOC2007.pkl2', 'rb') as f:
    #with open('TLD201803.pkl', 'rb') as f:
    #with open('prior_boxes_ssd300.pkl', 'rb') as f:
    with open('TLD201803-4.p', 'rb') as f:
        #u = pickle._Unpickler(f)
        #u.encoding = 'latin1'
        #data = u.load()
        data = pickle.load(f)
        print(data)
