#----------------------------------------------#
# Autonomous Vehicle Machine Vision System     #
# Machine Vision System                        #
# lineDetection.py                             #
# Written by:                                  #
# Jeremy Beauchamp, Zhaojie Chen,              #
# Trenton Davis, and Xudong Yuan               # 
#----------------------------------------------#

'''
This file contains if there is line detection and where it is.
'''

import cv2
import numpy as np

# LineDetection class
################################################################################
class LineDetection:
	'''
	The LineDetection class is the class we implemented to detect lines from the image.
	'''
	def __init__(self):
		'''
		Initializes the line detection.
		'''
		self.lowerWhite = np.array([0, 150, 0])
		self.upperWhite = np.array([255, 255, 255])
		self.lowerYellow = np.array([0, 200, 200])
		self.upperYellow = np.array([215, 255, 255])
		self.kernel = np.ones((5, 5), np.uint8)
		
	def convertToHSV(self, frame):
		'''
		Formats the array of pixels to be in HSV format.
		'''
		return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		
	def convertToHLS(self, frame):
		'''
		Formats the array of pixels to be in HLS format.
		'''
		return cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
		
	def yellowLines(self, frame):
		'''
		Will detect yellow line, and its position.
		'''
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(frame, self.lowerYellow, self.upperYellow)
		res = cv2.bitwise_and(frame, frame, mask = mask)
		res  = cv2.GaussianBlur(res, (15, 15), 0)
		res = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
		res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(res, 50, 100)
		lines = cv2.HoughLinesP(edges, 1, np.pi/180, 60, 50, 10)
		
		topLeft = []
		topRight = []
		bottomLeft = []
		bottomRight = []
		if lines is None:
			pass
		else:
			for line in lines:
				for x1, y1, x2, y2 in line:
					if x1 < 320 and y1 < 240:
						topLeft.append(line)
					elif x1 >= 320 and y1 < 240:
						topRight.append(line)
					elif x1 < 320 and y1 >= 240:
						bottomLeft.append(line)
					else:
						bottomRight.append(line)
						
		l = [topLeft, topRight, bottomLeft, bottomRight]
		slope = [0.0, 0.0, 0.0, 0.0]
		distance = [0, 0, 0, 0]
		count = [0, 0, 0, 0]
		left = False
		right = False
		for i in range(len(l)):
			yMax = 0
			yMin = 1000
			for line in l[i]:
				count[i] += 1
				s = 0
				for x1, y1, x2, y2 in line:
					s = (y2 - y1) / (x2 - x1)
					if y1 > yMax:
						yMax = y1
					if y2 > yMax:
						yMax = y2
					if y1 < yMin:
						yMin = y1
					if y2 < yMin:
						yMin = y2
				slope[i] += s
			distance[i] = yMax - yMin
			if distance[i] > 0:
				slope[i] /= count[i]
		if distance[0] + distance[2] >= 200:
			left = True
		else:
			left = False
		if distance[1] + distance[3] >= 200:
			right = True
		else:
			right = False
		'''
		We do a tangent to each point on the line to 
		determine whether to go straight or turn
		'''	
		if left and slope[0] >= 0.0 and slope[2] < 0.0:
			leftTurn = True
		elif right and slope[1] < slope[3] / 2:
			leftTurn = True
		else:
			leftTurn = False
		if right and slope[1] <= 0.0 and slope[3] > 0.0:
			rightTurn = True
		elif left and slope[0] > slope[2] / 2:
			rightTurn = True
		else:
			rightTurn = False
		
		return left, right, leftTurn, rightTurn, lines
		
	def whiteLines(self, frame):
		'''
		Will detect white line, and its position.
		'''
		hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
		mask = cv2.inRange(hls, self.lowerWhite, self.upperWhite)
		res = cv2.bitwise_and(frame, frame, mask = mask)
		
		res = cv2.morphologyEx(res, cv2.MORPH_CLOSE, self.kernel)
		
		res  = cv2.GaussianBlur(res, (15, 15), 0)
		
		res = cv2.cvtColor(res, cv2.COLOR_HLS2BGR)
		res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
		
		edges = cv2.Canny(res, 50, 100)

		lines = cv2.HoughLinesP(edges, 1, np.pi/180, 75, 50, 10)
		
		topLeft = []
		topRight = []
		bottomLeft = []
		bottomRight = []
		if lines is None:
			pass
		else:
			for line in lines:
				for x1, y1, x2, y2 in line:
					if x1 < 320 and y1 < 240:
						topLeft.append(line)
					elif x1 >= 320 and y1 < 240:
						topRight.append(line)
					elif x1 < 320 and y1 >= 240:
						bottomLeft.append(line)
					else:
						bottomRight.append(line)
						
		l = [topLeft, topRight, bottomLeft, bottomRight]
		slope = [0.0, 0.0, 0.0, 0.0]
		distance = [0, 0, 0, 0]
		count = [0, 0, 0, 0]
		left = False
		right = False
		for i in range(len(l)):
			yMax = 0
			yMin = 1000
			for line in l[i]:
				count[i] += 1
				s = 0
				for x1, y1, x2, y2 in line:
					s = (y2 - y1) / (x2 - x1)
					if y1 > yMax:
						yMax = y1
					if y2 > yMax:
						yMax = y2
					if y1 < yMin:
						yMin = y1
					if y2 < yMin:
						yMin = y2
				slope[i] += s
			distance[i] = yMax - yMin
			if distance[i] > 0:
				slope[i] /= count[i]
		if distance[0] + distance[2] >= 200:
			left = True
		else:
			left = False
		if distance[1] + distance[3] >= 200:
			right = True
		else:
			right = False
		'''
		We do a tangent to each point on the line to 
		determine whether to go straight or turn
		'''
		if left and slope[0] >= 0.0 and slope[2] < 0.0:
			leftTurn = True
		elif right and slope[1] < slope[3] / 2:
			leftTurn = True
		else:
			leftTurn = False
		if right and slope[1] <= 0.0 and slope[3] > 0.0:
			rightTurn = True
		elif left and slope[0] > slope[2] / 2:
			rightTurn = True
		else:
			rightTurn = False
		
		return left, right, leftTurn, rightTurn, lines

	def finishLines(self, frame):
		'''
		Will detect the final line, and its position.
		'''
		src = frame
		gray_src = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray_src = cv2.bitwise_not(gray_src)
		binary_src = cv2.adaptiveThreshold(gray_src, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
		hline = cv2.getStructuringElement(cv2.MORPH_RECT, ((binary_src.shape[1] // 10), 1), (-1, -1))
		nothing = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
		vline = cv2.getStructuringElement(cv2.MORPH_RECT, (1, (binary_src.shape[0] // 16)), (-1, -1))
		dst = cv2.morphologyEx(binary_src, cv2.MORPH_OPEN, hline)
		dst = cv2.bitwise_not(dst)
		count = 0
		fd = False
		edges = cv2.Canny(dst,50,150,apertureSize = 3)
		lines = cv2.HoughLinesP(edges,1,np.pi/180,30,minLineLength=60,maxLineGap=10)
		if lines is None:
			fd = False
		elif (lines.any() != None):
			lines1 = lines[:,0,:]
			for x1,y1,x2,y2 in lines1[:]:
				count = count + 1
		if count > 10:
			fd = True
		return fd, lines
