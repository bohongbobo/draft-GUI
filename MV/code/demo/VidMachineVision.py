#----------------------------------------------#
# Autonomous Vehicle Machine Vision System     #
# Machine Vision System                        #
# machineVision.py                             #
# Written by:                                  #
# Jeremy Beauchamp, Zhaojie Chen,              #
# Trenton Davis, and Xudong Yuan               # 
#----------------------------------------------#

'''
This file contains the overall Machine Vision System as well as any constants that
are necessary. All of the functionality of the whole system is contained in this 
single file.
'''

# Import libraries
import time
import threading
from queue import Queue
import cv2

# Import modules
import imageData as imd
import gui as g
import stabilizer as s
import enhancer as e
import objects as o
import event as ev
import trafficLightDetector as tld
import yellowline_detection as yd


# MachineVision Class
################################################################################
class MachineVision:
	'''
	The MachineVision class is the overall class that contains the Autonomous
	Vehicle Machine Vision System.

	:ivar camera: the camera used to capture images
	:ivar gui: the GUI that displays the images
	:ivar stabilizer: the video stabilizer
	:ivar enhancer: the image enhancer
	:ivar BufferSize: the amount of images stored in the buffer
	:ivar ImageBuffer: the buffer storing images
	:ivar BufferIndex: the current index in the buffer
	'''

	def __init__(self, video, objectSet = []):
		'''
		Creates all variables.

		:type camera: Camera object
		:param camera: the camera used for capturing images
		'''
		self.cap = cv2.VideoCapture(video)
		self.gui = g.GUI()
		self.stabilizer = s.Stabilizer()
		self.enhancer = e.Enhancer()
		self.event = ev.Event(objectSet)
		self.trafficLightNN = tld.TrafficLightDetector()
		LookoutRange = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5.5, 6.5, 7.5] #[1.5, 2.5, 3.5, 5, 7]# 
		Region_WB = [250, 270, 360, 380]
		self.line_detec = yd.yellowline(self.cap, LookoutRange, Region_WB)

		self.current = 0
		self.BufferSize = 0
		self.ImageBuffer = []
		self.BufferIndex = 0
		
		self.printLock = threading.Lock()
		self.trafficLock = threading.Lock()
		self.lineLock = threading.Lock()
		self.q = Queue()

	def initialize(self):
		'''
		Creates image buffer and activates the camera and GUI.
		'''

		self.BufferSize = 15
		self.ImageBuffer = []
		for i in range (self.BufferSize):
			self.ImageBuffer.append(imd.ImageData(0))

		self.stabilizer.smoothingWindow = self.BufferSize

		self.gui.activate()
		self.trafficLightNN.activate()
		
		#self.enhancer.x = self.camera.RES[0]
		#self.enhancer.y = self.camera.RES[1]
		self.enhancer.x = 640
		self.enhancer.y = 480
		
		for i in range (2):
			self.q.put(i)

	def shutdown(self):
		'''
		Shutsdown the camera and GUI.
		'''
		
		if(self.gui.active):
			self.gui.deactivate()
			
	def detectTrafficLight(self):
		'''
		Detects if there is a traffic light presetn.
		'''
		while(True):
			res1, res2 = self.trafficLightNN.detect(self.current)
			self.event.objects[0].active = res1
			self.event.objects[0].green = res2
			
	def detectYellowLines(self):
		'''
		Detects if there are yellow lines on the screen.
		'''
		while(True):
			_,res1,res2,res3,res4,res5 = self.line_detec.line_detec(self.current)
			self.event.objects[1].active = res1
			self.event.objects[1].leftLine = res2
			self.event.objects[1].rightLine = res3
			self.event.objects[1].turning = res4
			self.event.objects[1].turnRight = res5
	
	def assignJob(self):
		'''
		Assigns jobs for the multithreading to work.
		'''
		i = self.q.get()
		if(i == 0):
			self.detectTrafficLight()
		elif(i == 1):
			self.detectYellowLines()
		self.q.task_done()
		
	def oneLoop(self):
	
		self.current = imd.ImageData(self.camera.capture())

		self.current.frame = self.enhancer.enhance(self.current)
				
	#	if(self.BufferIndex > 1):
	#		previous = self.ImageBuffer[self.BufferIndex - 1]
	#		self.current.frame = self.stabilizer.stabilize(previous, self.current)
				
		for i in range (2):
			t = threading.Thread(target = self.assignJob)
			t.daemon = True
			t.start()
					
		if(self.event.objects[0].active):
			print("Light Detected")
			if(self.event.objects[0].green):
				print("Green")
		else:
			print()

	#	if(self.gui.active):
	#		self.gui.display(self.current)
				
		self.ImageBuffer[self.BufferIndex] = self.current
		self.BufferIndex = self.BufferIndex + 1
		if(self.BufferIndex >= self.BufferSize):
			self.BufferIndex = 0
				
		return self.current, self.event.convert()
				
	def run(self):
		'''
		Runs the entire Machine Vision System.
		'''

		self.initialize()

		timePerFrame = 1.0 / 15
		self.current = imd.ImageData(0)
		previous = imd.ImageData(0)

		try:

			while(self.cap.isOpened()):
				start = time.time()
				
				_, image = self.cap.read()
				self.current = imd.ImageData(image)

				self.current.frame = self.enhancer.enhance(self.current)
				
			#	if(self.BufferIndex > 1):
			#		previous = self.ImageBuffer[self.BufferIndex - 1]
			#		self.current.frame = self.stabilizer.stabilize(previous, self.current)
					
				for i in range (2):
					t = threading.Thread(target = self.assignJob)
					t.daemon = True
					t.start()
					
				if(self.event.objects[0].active):
					print("Light Detected")
					if(self.event.objects[0].green):
						print("Green")
				else:
					print()

				if(self.gui.active):
					self.gui.display(self.current)
				else:
					break
				
				self.ImageBuffer[self.BufferIndex] = self.current
				self.BufferIndex = self.BufferIndex + 1
				if(self.BufferIndex >= self.BufferSize):
					self.BufferIndex = 0
					
				end = time.time()
				if((end - start) < timePerFrame):
					time.sleep(timePerFrame - (end - start))

		except KeyboardInterrupt:
			pass

		self.shutdown()

################################################################################
