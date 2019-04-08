#----------------------------------------------#
# Autonomous Vehicle Machine Vision System     #
# Object Classes                               #
# objects.py                                   #
# Written by:                                  #
# Jeremy Beauchamp, Zhaojie Chen,              #
# Trenton Davis, and Xudong Yuan               # 
#----------------------------------------------#

'''
This file contains all objects than can be recognized by the Machine Vision System.
'''

# TrafficLight Class
################################################################################
class TrafficLight:
	'''
	The TrafficLight class represent a traffic light detected by the vision system.
	
	:ivar active: boolean respresenting if a light has been detected
	:ivar green: boolean representing if the light is green or not
	'''

	def __init__(self):
		'''
		Constructor that simply sets the default value for green to False
		'''

		self.active = False
		self.green = False


	def convert(self):
		'''
		Converts the state of green into a string and returns it.
		'''
		if(self.active):
			if(self.green):
				return "11"
			else:
				return "10"
		else:
			return "00"

################################################################################

# Lines Class
################################################################################
class Lines:
	'''
	The Lines class contains all of the parameters that are to be expected when the
	car detects a line, as well as a way to encode the data to pass to the cognitive state machine.
	'''

	def __init__(self):
		'''
		Initializes the line object to its default parameters.
		'''
		self.active = False
		self.leftLine = False
		self.rightLine = False
		self.distanceLeft = 0.0
		self.distanceRight = 0.0
		self.turning = False
		self.turnRight = False
		self.turnAngle = 0.0


	def convert(self):
		'''
		Converts to data that will be passed to the cognitive state machine.
		'''
		string = ""
		if(self.active):
			string = string + "1"
			if(self.leftLine):
				string = string + "1"
			else:
				string = string + "0"
			if(self.rightLine):
				string = string + "1"
			else:
				string = string + "0"
			if(self.turning):
				string = string + "1"
				if(self.turnRight):
					string = string + "1"
				else:
					string = string + "0"
			else:
				string = string + "00"
			return string
		else:
			return "00000"
			
################################################################################

# FinishLine Class
################################################################################
class FinishLine:
	'''
	The FinishLine class contains all of the parameters that are to be expected when
	the car detects a finish line, as well as a convert function that will send information
	to the cognitive state machine.
	'''

	def __init__(self):
		'''
		Initializes the finish line to not being present.
		'''
		self.active = False
		self.distance = 0.0


	def convert(self):
		'''
		Converts to data that will be passed to the cognitive state machine.
		'''
		if(self.active):
			return "1"
		else:
			return "0"

################################################################################

# Obstacle Class
################################################################################
class Obstacle:
	'''
	The Obstacle class contains all of the parameters that are to be expected when
	the car detects an object, as well as a convert function that will send information
	to the cognitive state machine.
	'''

	def __init__(self):
		'''
		Initializes the obstace to not being present.
		'''
		self.active = False
		self.distance = 0.0
		self.width = 0.0
		self.distanceFromLeft = 0.0
		self.distanceFromRight = 0.0


	def convert(self):
		'''
		Converts to data that will be passed to the cognitive state machine.
		'''
		if(self.active):
			return "1"
		else:
			return "0"

################################################################################

# Car Class
################################################################################
class Car:
	'''
	The Car class contains all of the parameters that are to be expected when
	the car detects another car, as well as a convert function that will send information
	to the cognitive state machine.
	'''

	def __init__(self):
		'''
		Initializes to a car not being present.
		'''
		self.active = False
		self.gaining = False
		self.distance = 0.0
		self.distanceFromLeft = 0.0
		self.distanceFromRight = 0.0
		self.speed = 0.0


	def convert(self):
		'''
		Converts to data that will be passed to the cognitive state machine.		
		'''
		if(self.active):
			if(self.gaining):
				return "11"
			else:
				return "10"
		else:
			return "00"

################################################################################

# Arrow Class
################################################################################
class Arrow:
	'''
	The Arrow class contains all of the parameters that are to be expected when the car 
	detects a turn arrow, as well as a convert function that will send information to the 
	cognitive state machine.
	'''

	def __init__(self):
		'''
		Initializes arrows to not be present.
		'''
		self.active = False
		self.leftArrow = False
		self.rightArrow = False
		self.upArrow = False
		self.leftDist = 0.0
		self.rightDist = 0.0


	def convert(self):
		'''
		Converts to data that will be passed to the cognitive state machine.
		'''
		if(self.active):
			if(self.leftArrow):
				if(self.rightArrow):
					if(self.upArrow):
						return "1111"
					else:
						return "1110"
				else:
					if(self.upArrow):
						return "1101"
					else:
						return "1100"
			else:
				if(self.rightArrow):
					if(self.upArrow):
						return "1011"
					else:
						return "1010"
				else:
					if(self.upArrow):
						return "1001"
					else:
						return "1000"
		else:
			return "0000"

################################################################################





