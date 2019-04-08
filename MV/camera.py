#----------------------------------------------#
# Autonomous Vehicle Machine Vision System     #
# Camera Interface                             #
# camera.py                                    #
# Written by:                                  #
# Jeremy Beauchamp, Zhaojie Chen,              #
# Trenton Davis, and Xudong Yuan               # 
#----------------------------------------------#

'''
This file contains the Camera class, which allows access to the stream of video
provided by a camera device. This file also contains two premade cameras that 
represent the testing webcam, and the actual camera on the Autonomous Vehicle.
'''

# Import libraries
import numpy as np
import cv2

# Camera Class
################################################################################
class Camera:
	'''
	The Camera class contains all of the information and functionality needed to
	use an external camera and obtain frames from it.
	
	:ivar MAX_FPS: maximum frame rate of the camera
	:ivar MAX_RES: maximum resolution of the camera
	:ivar FPS: current rate at which frames are captured at
	:ivar RES: current resolution at which frames are being captured with
	:ivar CAP: the connection to the camera
	'''

	def __init__(self, fps = 0, res = [0, 0], video = 0):
		'''
		Constructor for the Camera class.

		:type fps: int
		:param fps: the maximum frame rate of the camera

		:type res: list of two ints
		:param fps: the maximum resolution of the camera in the from [W, H]

		:type external: bool
		:param external: if an external device is used it is true, otherwise it 
						 is assumed that an internal device is used
		'''

		self.MAX_FPS = fps
		self.MAX_RES = res
		self.FPS = fps
		self.RES = res
		self.VID = video
		self.CAP = cv2.VideoCapture()


	def activate(self):
		'''
		Activates camera.
		'''
		self.CAP = cv2.VideoCapture(self.VID)
		self.setExposure()


	def deactivate(self):
		'''
		Shuts down the webcam.
		'''

		self.CAP.release()
		cv2.destroyAllWindows()


	def setExposure(self):
		'''
		Set the exposure level of the camera.
		'''

		self.CAP.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
		self.CAP.set(cv2.CAP_PROP_EXPOSURE, -7.0)


	def setFPS(self, fps):
		'''
		Sets rate at which frames are captured from the webcam.

		:type fps: int
		:param fps: the desired capture rate
		'''

		if(fps <= self.MAX_FPS):
			self.FPS = fps
			self.CAP.set(cv2.CAP_PROP_FPS, self.FPS)
		else:
			self.FPS = self.MAX_FPS


	def setRES(self, res):
		'''
		Sets resolution at which frames are captured.

		:type res: list of two ints
		:param res: the desired resolution
		'''

		if(res[0] <= self.MAX_RES[0] and res[1] <= self.MAX_RES[1]):
			self.RES = res
			self.CAP.set(cv2.CAP_PROP_FRAME_WIDTH, self.RES[0])
			self.CAP.set(cv2.CAP_PROP_FRAME_HEIGHT, self.RES[1])
		else:			
			self.RES = self.MAX_RES


	def capture(self):
		'''
		Captures a single frame and returns it.
		'''

		check, frame = self.CAP.read()
		if(check):
			return frame
		else:
			return 0


################################################################################
