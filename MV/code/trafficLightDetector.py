#----------------------------------------------#
# Autonomous Vehicle Machine Vision System     #
# Traffic Light Detection                      #
# lightDetection.py                            #
# Written by:                                  #
# Yichao Li                                    #
# Modified by:                                 #
# Jeremy Beauchamp, Zhaojie Chen,              #
# Trenton Davis, and Xudong Yuan               # 
#----------------------------------------------#

'''
This file contains the algorithm to detect traffic lights and determine if they
are or are not green. This done using TensorFlow.
'''

import tensorflow as tf
import numpy as np
import cv2
from utils import label_map_util

# TrafficLightDetector class
################################################################################
class TrafficLightDetector:
	'''
	The TrafficLightDetector class contains all of the required set up and detection
	functions required to determine if a traffic light is present and if it is green
	or not.

	:ivar pathCKPT: path to the frozen neural network
	:ivar pathLabels: path to the labels for traffic lights
	:ivar numClasses: number of classes used
	:ivar sess: current tensorflow session
	'''

	def __init__(self, PATH_TO_CKPT = "tf/frozen_inference_graph.pb", PATH_TO_LABELS = "tf/traffic_light.pbtxt"):
		'''
		Sets the paths to any necessary files for the neural network to function
		'''

		self.pathCKPT = PATH_TO_CKPT
		self.pathLabels = PATH_TO_LABELS
		self.numClasses = 3


	def activate(self):
		'''
		Performs all of the operations to set up the neural network before the execution
		of the program. This is only required once per session.
		'''

		detection_graph = tf.Graph()
		with detection_graph.as_default():
			od_graph_def = tf.GraphDef()
			with tf.gfile.GFile(self.pathCKPT, "rb") as fid:
				serialized_graph = fid.read()
				od_graph_def.ParseFromString(serialized_graph)
				tf.import_graph_def(od_graph_def, name = '')
		label_map = label_map_util.load_labelmap(self.pathLabels)
		categories = label_map_util.convert_label_map_to_categories(label_map, self.numClasses, use_display_name = True)
		category_index = label_map_util.create_category_index(categories)
		boxes_list = []
		with detection_graph.as_default():
			self.sess = tf.Session(graph=detection_graph)
			self.image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
			self.detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
			self.detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
			self.detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
			self.num_detections = detection_graph.get_tensor_by_name('num_detections:0')

	def detect(self, image):
		'''
		Uses the neural network to determine if a traffic light is in frame. If
		the certainty is greater than 50%, then it is assumed that a traffic light
		is present. The first bool returned is true if a traffic light is detected,
		and the second bool is true if the light is green.

		:type image: imageData
		:param image: the imageData object to be analyzed
		'''

		frame = image.frame
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		hsv[0] = hsv[0] + 15
		image_cv2 = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
		image_np_expanded = np.expand_dims(image_cv2, axis = 0)
		(boxes, scores, classes, num) = self.sess.run([self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections], feed_dict = {self.image_tensor: image_np_expanded})

		if scores[0][0] > 0.5:
			if classes[0][0] == 2:
				return True, True
			else:
				return True, False
		else:
			return False, False
		
################################################################################
