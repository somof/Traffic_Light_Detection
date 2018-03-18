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

    opencv_annotation -i=/to/images/folder -a=annotation.txt
    python gt_format.py

# training

    cd ssd
	python SSD_train.py


# TLD documentation

## Traffic Light Detection

The traffic light detection node is responsible for selecting next waypoionts for upcoming traffic signals and stop lines.
In addition, it needs to classify the traffic signal's state like red, green, yellow or unknow.

input
sub1 = rospy.Subscriber('/current_pose',
    PoseStamped,
    self.pose_cb -> get msg

sub2 = rospy.Subscriber('/base_waypoints',
    Lane,
    self.waypoints_cb -> get waypoints and psitions

sub3 = rospy.Subscriber('/vehicle/traffic_lights',
    TrafficLightArray,
    self.traffic_cb ->  get msg.lights

sub6 = rospy.Subscriber('/image_color',
    Image,
    self.image_cb

publish
    self.upcoming_red_light_pub = rospy.Publisher('/traffic_waypoint', Int32, queue_size=1)

image_cb()
    control behavir about traffic light state and position


process_traffic_lights()
    if find visible traffic light , classify it

### Traffic Light Recognition

### Traffic Light Classification
Once the traffic light detection node finds upcoming visible traffic lights,
it calls a classification method in Traffic Light Classification class (TLClassifier).
This method has a camera image argument for input from ROS messages and returns the current color state of the traffic lights.

To recognize the color state, the method detects the traffic light area in the image and classifies with its signal color state at once with a DeepLearning technique called 'Single Shot MultiBox Detector',




two funtions are needed


DeepLearning is a successful technique to accomplish the two 

classify

and detects traffic light areas and thier state as 


#### Dataset for Traffic Light detection

Traffic Light detection

# SSD for Traffic Light Detection

For more details, please refer to 

- [SSD: Single Shot MultiBox Detector](https://github.com/weiliu89/caffe/tree/ssd)
- [arXiv paper](http://arxiv.org/abs/1512.02325).



<!-- ### Traffic Light Recognition -->
<!-- ### Traffic Light Classification -->

