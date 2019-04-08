#----------------------------------------------#
# Autonomous Vehicle Machine Vision System     #
# Traffic Light Detection                      #
# lightDetection.py                            #
# Written by:                                  #
# Letian Lin                                   #
# Modified by:                                 #
# Jeremy Beauchamp, Zhaojie Chen,              #
# Trenton Davis, and Xudong Yuan               # 
#----------------------------------------------#
#-------------------------------------------------------
# In this file, the lane data in the camera frame are
# converted to those in the body frame 
# Input: 
# Lane data (int) in the camera frame from the vision system
# Output:
# Lane data (float) in the body frame
#-------------------------------------------------------
 
import numpy as np

# The resolution of the camera is 640*480
x_max = 640
y_max = 480
# Paramters
h = 0.305 # height of the camera 
alpha_cam = 0.3 # tilt-down angle 0.15
alpha_y = 0.39 # vertical half-angle of view 
d = 0.19 # distance from the center of the camera to the CG

#---------------------------------------------------
# The following function converts a point in camera 
# frame to that in body frame
#---------------------------------------------------
 
def CamToBody_pt(point_cam):
    if len(point_cam) > 0:
        x_cam = point_cam[0]
        y_cam = point_cam[1]
        x_b = h/np.tan(np.arctan(np.tan(alpha_y)/240*(y_cam-240)) + alpha_cam) + d
        y_b = (x_cam - 320)/np.sqrt((240/np.tan(alpha_y))**2+(y_cam-240)**2) * np.sqrt(x_b**2 + h**2)
        point_b = [x_b, y_b]
    else:
        point_b = []
    return point_b
    
#---------------------------------------------------
# The following function converts a point in body 
# frame to that in camera frame
#---------------------------------------------------

def BodyToCam_pt(point_b):
    if len(point_b) > 0:
        x_b = point_b[0]
        y_b = point_b[1]
        f = 240/np.tan(alpha_y)
        y_cam = np.tan(np.arctan(h/(x_b-d)) - alpha_cam)*f + 240
        x_cam = y_b * np.sqrt(f**2+(y_cam-240)**2) / np.sqrt(x_b**2 + h**2) + 320
        point_cam = [int(x_cam), int(y_cam)]
    else:
        point_cam = []
    return point_cam

#--------------------------------------------------------
# The following function converts the lane points in 
# the camera frame to that in body frame
# The input points are of the form: [[x1, x2, x3],[y1, y2, y3]]
# The output points are of the form: [[x1, y1], [x2, y2], [x3, y3]]
#--------------------------------------------------------

def CamToBody(left_point,right_point): 
    left_point = np.array(left_point)
    right_point = np.array(right_point)
    if len(left_point.shape) > 1:
        n_left = len(left_point[0]) # number of left points
        left_point_b = []
        for i in range(n_left):
            point_b_left = CamToBody_pt([left_point[0][i],left_point[1][i]])
            left_point_b.append(point_b_left)
    elif len(left_point)>0:
        point_b_left = CamToBody_pt([left_point[0],left_point[1]])
        left_point_b = point_b_left
    else:
        left_point_b = np.array([])
        
    if len(right_point.shape) > 1:
        n_right = len(right_point[0]) # number of right points
        right_point_b = []
        for i in range(n_right):
            point_b_right = CamToBody_pt([right_point[0][i],right_point[1][i]])
            right_point_b.append(point_b_right)
    elif len(right_point)>0:
        point_b_right = CamToBody_pt([right_point[0],right_point[1]])
        right_point_b = point_b_right
    else:
        right_point_b = np.array([])
        
    return left_point_b, right_point_b
    
#--------------------------------------------------------
# The following function converts the lane points in 
# the body frame to that in camera frame
# The input points are of the form: [[x1, y1], [x2, y2], [x3, y3]]
# The output points are of the form: [[x1, y1], [x2, y2], [x3, y3]]
#--------------------------------------------------------

def BodyToCam(left_point_b,right_point_b): 
    left_point_b = np.array(left_point_b)
    right_point_b = np.array(right_point_b)
    
    if len(left_point_b.shape) > 1:
        n_left = len(left_point_b[:,0]) # number of left points
        left_point_cam = []
        for i in range(n_left):
            point_cam_left = BodyToCam_pt([left_point_b[i][0],left_point_b[i][1]])
            left_point_cam.append(point_cam_left)
    else:
        point_cam_left = BodyToCam_pt([left_point_b[0],left_point_b[1]])
        left_point_cam = point_cam_left
        
    if len(right_point_b.shape) > 1:
        n_right = len(right_point_b[:,0]) # number of right points
        right_point_cam = []
        for i in range(n_right):
            point_cam_right = BodyToCam_pt([right_point_b[i][0],right_point_b[i][1]])
            right_point_cam.append(point_cam_right)
    else:
        point_cam_right = BodyToCam_pt([right_point_b[0],right_point_b[1]])
        right_point_cam = point_cam_right
    return left_point_cam, right_point_cam
