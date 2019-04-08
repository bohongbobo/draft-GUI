#----------------------------------------------#
# Autonomous Vehicle Machine Vision System     #
# Video Stabilizer                             #
# stabilizer.py                                #
# Written by:                                  #
# Jeremy Beauchamp, Zhaojie Chen,              #
# Trenton Davis, and Xudong Yuan               # 
#----------------------------------------------#

'''
This file contains the Stabilizer class, which contains everything to stabilize
the video stream from the camera.
'''

# Import libraries
import cv2
import numpy as np

# Stabilizer Class
################################################################################
class Stabilizer:
	'''
	The Stabilizer class performs a stabilization algorithm on the current frame
	that is based on the previous frame. 

	:ivar featureParams: the parameters feed into the goodFeaturesToTrack function
	:ivar opticalFlowParams: the parameters feed into the calcOpticalFlowPyrLK function
	:ivar smoothingWindow: the amount of frames to be averaged together
	:ivar xTrajectory: the movement from frame to frame in the X direction
	:ivar yTrajectory: the movement from frame to frame in the Y direction
	'''

	def __init__(self, window = 100):
		'''
		Initalizes smoothingWindow, xTrajectory, yTrajectory, and the parameters
		for optical flow and good features functions.
		'''

		self.featureParams = dict(maxCorners = 50, qualityLevel = 0.3,
								  minDistance = 7, blockSize = 7)
		self.opticalFlowParams = dict(winSize = (15, 15), maxLevel = 4,
									  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

		self.smoothingWindow = window
		self.xTrajectory = []
		self.yTrajectory = []

	def stabilize(self, old, new):
		'''
		Calculates the movement from frame to frame, calculates the average movement
		over the smoothing window, and warps the image.
		'''

		stable = new.frame
		gray = cv2.cvtColor(old.frame, cv2.COLOR_BGR2GRAY)
		rows, cols = gray.shape
		points = cv2.goodFeaturesToTrack(gray, mask = None, **self.featureParams)

		newGray = cv2.cvtColor(new.frame, cv2.COLOR_BGR2GRAY)

		if(points is not None):
			newPoints, match, err = cv2.calcOpticalFlowPyrLK(gray, newGray, points, None,
															 **self.opticalFlowParams)

			newGood = newPoints[match == 1]
			oldGood = points[match == 1]

			if(len(newGood) == 0 or len(oldGood) == 0):
				newGood = np.zeros((1, 2))
				oldGood = newGood

			transform = cv2.estimateRigidTransform(newGood, oldGood, False)
			if(transform is not None):
				xShift = transform[0, :]
				yShift = transform[1, :]
				self.xTrajectory.append(xShift)
				self.yTrajectory.append(yShift)

				if(len(self.xTrajectory) >= self.smoothingWindow):
					self.xTrajectory.pop(0)
					self.yTrajectory.pop(0)

				if(len(self.xTrajectory) > 0):
					xAvg = sum(self.xTrajectory) / len(self.xTrajectory)
					yAvg = sum(self.yTrajectory) / len(self.yTrajectory)
	
				trajectory = np.ndarray((2,3), buffer = np.array([xShift, yShift]))
				trajectoryAvg = np.ndarray((2,3), buffer = np.array([xAvg, yAvg]))
				delta = trajectoryAvg - trajectory
				newTransform = transform + delta
	
				stable = cv2.warpAffine(new.frame, newTransform, (cols, rows), flags = cv2.INTER_NEAREST|cv2.WARP_INVERSE_MAP)

		return stable

			


################################################################################
