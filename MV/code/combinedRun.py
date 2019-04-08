#!/usr/bin/env python3

import machineVision as mv
import camera as c
import objects as o

# CONSTANTS
#//////////////////////////////////////////////////////////////////////////////#
## Cameras ##
webcam = c.Camera(fps = 30, res = [1280, 720], video = 0)	#Testing webcam
vehicle = c.Camera(fps = 60, res = [1280, 720], video = 0)	#Vehicle camera

## Object Sets ##
allObjects = [o.TrafficLight(), o.Lines(), o.FinishLine(), o.Obstacle(), o.Car(), o.Arrow()]
#//////////////////////////////////////////////////////////////////////////////#


options = dict(camera = webcam,
			   objectSet = allObjects)

AVMVS = mv.MachineVision( **options)
AVMVS.initialize()

while(True):
	image, event = AVMVS.oneLoop()
	#State Machine stuff
	#info = SM(event)
	AVMVS.gui.display(image)
	print(event)
	#SM.gui.display(info)
	#for i in range(2):
	#	AVMVS.q.put(i)
