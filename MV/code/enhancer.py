#----------------------------------------------#
# Autonomous Vehicle Machine Vision System     #
# Image Enhancer                               #
# enhancer.py                                  #
# Written by:                                  #
# Jeremy Beauchamp, Zhaojie Chen,              #
# Trenton Davis, and Xudong Yuan               # 
#----------------------------------------------#

'''
This file contains the image enhancement system of the Machine Vision System.
The Enhancer class is responsible for preprocessing the image and give the image
detection system a high quality image to work with.
'''

# Import libraries
import cv2
import numpy as np
import tkinter as tk
from PIL import Image
from PIL import ImageTk
from PIL import ImageDraw

# Enhancer Class
################################################################################
class Enhancer:
	'''
	The Enhancer class is responsible for all image preprocessing operations. It
	has a single variable that contains a frame, and multiple functions to perform
	various operations on the frame.
	:ivar frame: the frame to be operated on
	'''
	
	def __init__(self):
		'''
		Simply intializes the frame variable to 0.
		'''

		self.frame = 0
		self.x = 1280
		self.y = 720

	def convertToPIL(self):
		'''
		Converts a LAB image to PIL format.
		'''

		self.frame = Image.fromarray(self.frame)

	def initcrop(self):
		'''
		Takes in old image and crops it based on the provided coordinates.
		'''
		
		self.frame = self.frame.crop((0, 50, self.x, self.y - 50))

	def convertToLAB(self):
		'''
		Converts a BGR image to LAB format.
		'''

		self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2LAB)


	def convertToBGR(self):
		'''
		Converts a LAB image to BGR format.
		'''

		self.frame = cv2.cvtColor(self.frame, cv2.COLOR_LAB2BGR)

	def convertToCV2(self):
		'''
		Converts a PIL image to CV2 format.
		'''

		self.frame = np.array(self.frame)

	def polycrop(self):
		'''
		Crops the image into a pentagon shape to cut back on image processing.
		'''

		x, y = self.frame.size

		self.frame = self.frame.convert("RGBA")

		imArray = np.asarray(self.frame)

		# create mask(leftbot,bot,rightbot)
		polygon = [(0, y/2), (x/2, 0), (x, y/2), (x, y), (0, y)]
		maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
		ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
		mask = np.array(maskIm)

		# assemble new image (uint8: 0-255)
		newImArray = np.empty(imArray.shape,dtype='uint8')

		# colors (three first columns, RGB)
		newImArray[:,:,:3] = imArray[:,:,:3]

		# transparency (4th column)
		newImArray[:, :, 3] = mask*255

		# back to Image from numpy
		newIm = Image.fromarray(newImArray, "RGBA")
		x, y = newIm.size
		self.frame = Image.new('RGBA', newIm.size, (0,0,0))
		self.frame.paste(newIm, (0, 0, x, y), newIm)
		
	def gamma_correction(self):
		'''
		Adjusts the Gamma of an image by a factor of 0.5
		'''
		
		gamma = 0.75 # This is the place to change the correction that is undergone.

		power = 1.0 / gamma # In order to correct the gamma in the way you want to, you must take the inverse of the gamma
		table = np.array([((i / 255.0) ** power) * 255 # This changes the value of each pixel based on the given gamma
		for i in np.arange(0, 256)]).astype("uint8")

		self.frame = cv2.LUT(self.frame, table)


	def whitebalance(self):
		'''
		Apply grey world algorithm to make white balance to the image.
		'''
		self.frame = self.frame.transpose(2, 0, 1).astype(np.uint32)
		avgB = np.average(self.frame[0])
		avgG = np.average(self.frame[1])
		avgR = np.average(self.frame[2])
		avg = (avgB + avgG + avgR) / 3
		self.frame[0] = np.minimum(self.frame[0] * (avg / avgB), 255)
		self.frame[1] = np.minimum(self.frame[1] * (avg / avgG), 255)
		self.frame[2] = np.minimum(self.frame[2] * (avg / avgR), 255)
		self.frame = self.frame.transpose(1,2,0).astype(np.uint8)


	def contrastEnhancement(self):
		'''
		Apply contrast limited adaptive histogram to the LAB image.
		'''

		planes = cv2.split(self.frame)
		clahe = cv2.createCLAHE(clipLimit = 2.0)
		planes[0] = clahe.apply(planes[0])
		self.frame = cv2.merge(planes)


	def enhance(self, image):
		'''
		Converts image to LAB, applys all enhancement functions, and then converts
		the image back to BGR.

		:type image: ImageData object
		:param image: the image to be enhanced
		'''

		self.frame = image.frame
		
		self.convertToPIL()
		self.initcrop()
		self.polycrop()
		self.convertToCV2()
		self.whitebalance()
		self.gamma_correction()
		self.convertToLAB()
		self.contrastEnhancement()
		self.convertToBGR()

		return self.frame

################################################################################
	
