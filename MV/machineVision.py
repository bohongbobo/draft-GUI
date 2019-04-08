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
import numpy as np
import cv2
from queue import Queue

# Import modules
import camera as c
import imageData as imd
import gui as g
import stabilizer as s
import enhancer as e
import objects as o
import mvevent as ev
import trafficLightDetector as tld
import yellowline_detection as yd
import lineDetection as ld
from yolo3.yolo import YOLO

## Cameras ##
webcam = c.Camera(fps = 30, res = [1280, 720], video = 0)	#Testing webcam
vehicle = c.Camera(fps = 60, res = [1280, 720], video = 0)	#Vehicle camer

## Object Sets ##
allObjects = [o.TrafficLight(), o.Lines(), o.FinishLine(), o.Obstacle(), o.Car(), o.Arrow()]

options = dict(camera = webcam,
			   objectSet = allObjects)

video = dict(videoMode =True,
			 video = "straightline_raw.mp4",
			 camera = webcam,
			 objectSet = allObjects)


green_count = 0
mc = 0

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

	def __init__(self, videoMode = False, video = None, camera = c.Camera(), objectSet = []):
		'''
		Creates all variables.

		:type camera: Camera object
		:param camera: the camera used for capturing images
		'''
		if videoMode and (video is not None):
			self.videoMode = True
			self.cap = cv2.VideoCapture(video)
			self.camera = 0
		else:
			self.videoMode = False
			self.camera = camera
		self.gui = g.GUI()
		self.stabilizer = s.Stabilizer()
		self.enhancer = e.Enhancer()
		self.event = ev.MVEvent(objectSet)
		self.trafficLightNN = tld.TrafficLightDetector()
		self.yolo = YOLO()
		LookoutRange = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5.5, 6.5, 7.5] #[1.5, 2.5, 3.5, 5, 7]#
		Region_WB = [250, 270, 360, 380]
		self.line_detec = yd.yellowline(camera, LookoutRange, Region_WB)

		self.current = 0
		self.newFrame = 0
		self.previous = 0
		self.BufferSize = 0
		self.ImageBuffer = []
		self.BufferIndex = 0

		self.printLock = threading.Lock()
		self.trafficLock = threading.Lock()
		self.lineLock = threading.Lock()
		self.frameLock = threading.Lock()
		self.q = Queue()
		self.tasks = 0
		self.taskList = []
		self.color = np.array([0, 0, 0])

		self.lineDetection = ld.LineDetection()

	def initialize(self):
		'''
		Creates image buffer and activates the camera and GUI.
		'''
		if not self.videoMode:
			self.BufferSize = self.camera.FPS
		else:
			self.BufferSize = 10

		self.ImageBuffer = []
		for i in range (self.BufferSize):
			self.ImageBuffer.append(imd.ImageData(0))
		self.stabilizer.smoothingWindow = self.BufferSize

		if not self.videoMode:
			self.camera.activate()
		self.gui.activate()
		self.trafficLightNN.activate()

		if not self.videoMode:
			self.camera.setFPS(15)
	#	self.enhancer.x = self.camera.RES[0]
	#	self.enhancer.y = self.camera.RES[1]

		self.enhancer.x = 640
		self.enhancer.y = 480
		self.threads = [0, 0, 0, 0]
		self.previous = imd.ImageData(0)
		self.lines = None

	def shutdown(self):
		'''
		Shutsdown the camera and GUI.
		'''

		if not self.videoMode:
			self.camera.deactivate()

		if(self.gui.active):
			self.gui.deactivate()

	def detectTrafficLight(self):
		'''
		Detects if there is a traffic light presetn.
		'''
		res1, res2 = self.trafficLightNN.detect(self.current)
		self.event.objects[0].active = res1
		self.event.objects[0].green = res2

	def detectYellowLines(self):
		'''
		Detects if there are yellow lines on the screen(Blue).
		'''
		left, right, leftTurn, rightTurn, lines = self.lineDetection.yellowLines(self.current.frame)
		self.event.objects[1].active = (left or right)
		self.event.objects[1].leftLine = left
		self.event.objects[1].rightLine = right
		self.event.objects[1].turning = (leftTurn or rightTurn)
		self.event.objects[1].turnRight = (rightTurn and (not leftTurn))

		self.frameLock.acquire()
		try:
			if lines is None:
				pass
			else:
				for line in lines:
					for x1, y1, x2, y2 in line:
						cv2.line(self.current.frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
		finally:
			self.frameLock.release()

	def detectWhiteLines(self):
		'''
		Detects if there are white lines on the screen(Red).
		'''
		left, right, leftTurn, rightTurn, lines = self.lineDetection.whiteLines(self.current.frame)
		self.event.objects[1].active = (left or right)
		self.event.objects[1].leftLine = left
		self.event.objects[1].rightLine = right
		self.event.objects[1].turning = (leftTurn or rightTurn)
		self.event.objects[1].turnRight = (rightTurn and (not leftTurn))

		self.frameLock.acquire()
		try:
			if lines is None:
				pass
			else:
				for line in lines:
					self.event.objects[1].active = True
					for x1, y1, x2, y2 in line:
						cv2.line(self.current.frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
						if x1 < (self.enhancer.x/2):
							self.event.objects[1].leftLine = True
						elif x1 > (self.enhancer.x/2):
							self.event.objects[1].rightLine = True
		finally:
			self.frameLock.release()

	def detectFinishLine(self):
		'''
		Detects if there are finish line on the screen.
		'''
		active, lines = self.lineDetection.finishLines(self.current.frame)
		self.event.objects[2].active = active
		self.frameLock.acquire()
		try:
			if lines is None:
				pass
			else:
				for line in lines:
					for x1, y1, x2, y2 in line:
						cv2.line(self.current.frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
		finally:
			self.frameLock.release()

	def detectImage(self):
		'''
		Detects arrows within an image.
		'''
		self.current.frame, temp = self.yolo.detect_image(self.current.frame,"print_all")

	def assignJob(self):
		'''
		Assigns jobs for the multithreading to work.
		'''
		i = self.q.get()
		if(i == 0):
			self.detectTrafficLight()
		elif(i == 1):
			self.detectYellowLines()
		elif(i == 2):
			self.detectWhiteLines()
		elif(i == 3):
			self.detectFinishLine()
		self.q.task_done()

	def turnOnTask(self, number):
		if(number not in self.taskList):
			self.taskList.append(number)
			self.tasks = self.tasks + 1

	def turnOffTask(self, number):
		if(number in self.taskList):
			self.taskList.remove(number)
			self.tasks = self.tasks - 1

	def getposBgr(self, event, x, y, flags, param):
		global mc
		if(mc == 1):
			return

		if event==cv2.EVENT_LBUTTONDOWN:
			self.color = self.current.frame[y, x]
			print("Bgr is", self.color)
			mc = 1
			#self.camera.deactivate()
			#self.run()
			#return

	def fillQueue(self):
		for t in self.taskList:
			self.q.put(t)

	def setTasks(self, currentTasks):
		current = 0
		for c in currentTasks:
			if(c == '1'):
				self.turnOnTask(current)
			else:
				self.turnOffTask(current)
			current = current + 1
		self.fillQueue()

	def getcolor(self):
		global mc
		#if(mc == 0):
		#	self.camera.activate()
		#self.current = imd.ImageData(0)
		#previous = imd.ImageData(0)
		if(mc == 0):
			if self.videoMode:
				_, image = self.cap.read()
				self.current = imd.ImageData(image)
			else:
				self.current = imd.ImageData(self.camera.capture())
			self.current.frame = self.enhancer.enhance(self.current)
			while(mc == 0):
				cv2.imshow('image', self.current.frame)
				cv2.setMouseCallback("image", self.getposBgr)
				if cv2.waitKey(0) ==ord('q'):
					cv2.destroyAllWindows()
		else:
			return
		self.lineDetection.lowerWhite[0] = self.color[0] - 50
		self.lineDetection.upperWhite[0] = self.color[0] + 50
		self.lineDetection.lowerYellow[0] = self.color[0] - 50
		self.lineDetection.upperYellow[0] = self.color[0] + 50
		self.lineDetection.lowerWhite[1] = self.color[1] - 50
		self.lineDetection.upperWhite[1] = self.color[1] + 50
		self.lineDetection.lowerYellow[1] = self.color[1] - 50
		self.lineDetection.upperYellow[1] = self.color[1] + 50
		self.lineDetection.lowerWhite[2] = self.color[2] - 50
		self.lineDetection.upperWhite[2] = self.color[2] + 50
		self.lineDetection.lowerYellow[2] = self.color[2] - 50
		self.lineDetection.upperYellow[2] = self.color[2] + 50
		self.current = imd.ImageData(0)

	def oneLoop(self, currentTasks):
		'''
		Executes one loop of the machine vision system.
		'''

		global green_count
		if self.videoMode:
			_, image = self.cap.read()
			self.current = imd.ImageData(image)
		else:
			self.current = imd.ImageData(self.camera.capture())

		self.current.frame = self.enhancer.enhance(self.current)

	#	if(self.BufferIndex > 1):
	#		self.previous = self.ImageBuffer[self.BufferIndex - 1]
	#		self.current.frame = self.stabilizer.stabilize(self.previous, self.current)
		self.detectImage()
		self.setTasks(currentTasks)
		for i in range (self.tasks):
			self.threads[i] = threading.Thread(target = self.assignJob)
			self.threads[i].daemon = True
			self.threads[i].start()
		for i in range(self.tasks):
			self.threads[i].join()

		self.ImageBuffer[self.BufferIndex] = self.current
		self.BufferIndex = self.BufferIndex + 1
		if(self.BufferIndex >= self.BufferSize):
			self.BufferIndex = 0

		if self.event.objects[0].active == True:
			if self.event.objects[0].green == True:
				if green_count >= 3:
					self.event.objects[0].green = True
					green_count += 1
				else:
					self.event.objects[0].green = False
					green_count += 1
			elif self.event.objects[0].green == False:
				green_count = 0
		elif self.event.objects[0].active == False:
			green_count = 0


		return self.current, self.event.convert()

	def run(self):
		'''
		Runs the entire Machine Vision System.
		'''
		global mc
		if(mc == 0):
			self.camera.activate()

		if not self.videoMode:
			timePerFrame = 1.0 / self.camera.FPS
		else:
			timePerFrame = 0

		self.current = imd.ImageData(0)
		previous = imd.ImageData(0)

		if self.videoMode:
			_, image = self.cap.read()
			self.current = imd.ImageData(image)
		else:
			self.current = imd.ImageData(self.camera.capture())

		if(mc == 0):
			self.current.frame = self.enhancer.enhance(self.current)
		while(mc == 0):
			cv2.imshow('image', self.current.frame)
			cv2.setMouseCallback("image", self.getposBgr)
			cv2.waitKey(0)
		self.initialize()
		self.lineDetection.lowerWhite[0] = self.color[0] - 50
		self.lineDetection.upperWhite[0] = self.color[0] + 50
		self.lineDetection.lowerYellow[0] = self.color[0] - 50
		self.lineDetection.upperYellow[0] = self.color[0] + 50
		self.lineDetection.lowerWhite[1] = self.color[1] - 50
		self.lineDetection.upperWhite[1] = self.color[1] + 50
		self.lineDetection.lowerYellow[1] = self.color[1] - 50
		self.lineDetection.upperYellow[1] = self.color[1] + 50
		self.lineDetection.lowerWhite[2] = self.color[2] - 50
		self.lineDetection.upperWhite[2] = self.color[2] + 50
		self.lineDetection.lowerYellow[2] = self.color[2] - 50
		self.lineDetection.upperYellow[2] = self.color[2] + 50

		try:

			while(True):
				start = time.time()

				if self.videoMode:
					_, image = self.cap.read()
					self.current = imd.ImageData(image)
				else:
					self.current = imd.ImageData(self.camera.capture())

				self.current.frame = self.enhancer.enhance(self.current)
			#	if(self.BufferIndex > 1):
			#		previous = self.ImageBuffer[self.BufferIndex - 1]
			#		self.current.frame = self.stabilizer.stabilize(previous, self.current)

				self.detectImage()
				self.setTasks('1111')
				for i in range (self.tasks):
					self.threads[i] = threading.Thread(target = self.assignJob)
					self.threads[i].daemon = True
					self.threads[i].start()
				for i in range(self.tasks):
					self.threads[i].join()

				print(self.event.convert())
				if(self.gui.active):
					self.gui.display(self.current)
				else:
					break

				self.ImageBuffer[self.BufferIndex] = self.current
				self.BufferIndex = self.BufferIndex + 1
				if(self.BufferIndex >= self.BufferSize):
					self.BufferIndex = 0
				end = time.time()
				print(end - start)
				if((end - start) < timePerFrame):
					time.sleep(timePerFrame - (end - start))

		except KeyboardInterrupt:
			pass

		self.shutdown()

################################################################################
