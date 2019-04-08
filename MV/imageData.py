#----------------------------------------------#
# Autonomous Vehicle Machine Vision System     #
# ImageData Class                              #
# imageData.py                                 #
# Written by:                                  #
# Jeremy Beauchamp, Zhaojie Chen,              #
# Trenton Davis, and Xudong Yuan               # 
#----------------------------------------------#

''' 
This file contains the ImageData for the Machine Vision System. This will be used 
as the main class to help altar the image.
'''

#imports libraries
import cv2
from PIL import Image
import numpy as np

#ImageData Class
################################################################################

class ImageData:
	''' 
	The ImageData class is used to store a frame and information about 
	that particular frame.

	:ivar frame: A frame that is received from the frame grabber
	'''

	def __init__(self, frame):
		'''
		Constructor for the ImageData class that sets the default to the frame.

		:type frame: array of ints
		:param frame: the frame that is received from the frame grabber
		'''

		self.frame = frame

################################################################################
