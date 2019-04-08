#!/usr/bin/env python3

import machineVision as mv
import camera as c
import objects as o

# CONSTANTS
#//////////////////////////////////////////////////////////////////////////////#
## Cameras ##
webcam = c.Camera(fps = 30, res = [1280, 720], video = 0)	#Testing webcam
vehicle = c.Camera(fps = 60, res = [1280, 720], video = 0)	#Vehicle camer

## Object Sets ##
allObjects = [o.TrafficLight(), o.Lines(), o.FinishLine(), o.Obstacle(), o.Car(), o.Arrow()]
#//////////////////////////////////////////////////////////////////////////////#


options = dict(videoMode = True,
			   video = "Speed_0.6_bandwidth_0.5.mp4",
			   camera = webcam,
			   objectSet = allObjects)

AVMVS = mv.MachineVision( **options)

AVMVS.run()
