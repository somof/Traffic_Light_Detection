[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)
This repository contains a SSD model made by reference to [cory8249](https://github.com/cory8249/ssd_keras.git).

# SSD for Traffic Light Detection

This is 'Traffic Light Detection' for System Integraton Project in Udacity 'Self-Driving Car Engineer Nanodegree Program'.

For more details, please refer to 

- [SSD: Single Shot MultiBox Detector](https://github.com/weiliu89/caffe/tree/ssd)
- [arXiv paper](http://arxiv.org/abs/1512.02325).

This code was tested with 

    Keras==2.0.8
    Pillow==2.2.1
    h5py==2.6.0
    numpy==1.13.1
    protobuf==3.5.2
    scipy==0.19.1
    tensorflow==1.3.0

# training images

    python bag_to_images.py bag/just_traffic_light.bag ssd/images /current_pose

# annotation data

    python gt_format.py

# training

    cd ssd
	python SSD_train.py
