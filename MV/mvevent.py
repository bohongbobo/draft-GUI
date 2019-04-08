#----------------------------------------------#
# Autonomous Vehicle Machine Vision System     #
# Event Class                                  #
# event.py                                     #
# Written by:                                  #
# Jeremy Beauchamp, Zhaojie Chen,              #
# Trenton Davis, and Xudong Yuan               # 
#----------------------------------------------#

'''
This file contains the Event class, which represents a point of interest detected
by the Machine Vision System.
'''

# Import modules
import objects as o

# Event Class
################################################################################
class MVEvent:
	'''
	The Event class contains all objects that are currently detected as well as
	a function to convert the data about the object into a string used by the 
	cognitive state machine.

	:ivar tl: represents a TrafficLight object. This will be changed in the future.
		      it is there simply as a proof of concept.
	'''

	def __init__(self, objectSet = []):
		'''
		Constructor that creates an empty list of Objects.
		'''
		
		self.objects = objectSet
		

	def convert(self):
		'''
		Converts all objects in the event to a single string and returns it.
		'''
		string = ""
		for i in range (len(self.objects)):
			string = string + self.objects[i].convert()

		return string

################################################################################
