#!/usr/bin/env python3

import VidMachineVision as mv
import camera as c
import objects as o

# CONSTANTS
#//////////////////////////////////////////////////////////////////////////////#
## Cameras ##
webcam = c.Camera(fps = 30, res = [1280, 720], video = 0)	#Testing webcam
vehicle = c.Camera(fps = 60, res = [1280, 720], video = 0)	#Vehicle camer

## Object Sets ##
allObjects = [o.TrafficLight(), o.Lines(), o.Obstacle(), o.Car(), o.FinishLine()]
#//////////////////////////////////////////////////////////////////////////////#

AVMVS = mv.MachineVision('traffic.avi', objectSet = allObjects)

AVMVS.run()
