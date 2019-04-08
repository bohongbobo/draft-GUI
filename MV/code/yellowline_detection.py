
# ----------------------------------------------------
# Changes in this version:
# 1.White balance
# 2 Edge detection from middle to side
# ---------------------------------------------------- 
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


import cv2
import numpy as np
import multiprocessing
import CamBodyConversion
import time
from scipy import stats


class yellowline():
    def __init__(self,cap,LookoutRange, Region_WB, vis_flag=True):
        self.cap = cap
        self.res1 = False
        self.res2 = False
        self.res3 = False
        self.res4 = False
        self.res5 = False
        self.num = 10
        self.Ym = [0]*self.num #[45, 50, 75, 100, 125]
        self.slice_width = 50
        self.mask_array = [-1]*self.num
        sensitivity = 20
        self.lower = np.array([30-sensitivity,40,80], dtype=np.uint8) # Saturation should be higher to filter out white
        self.upper = np.array([30+sensitivity, 255, 255], dtype=np.uint8)
#        self.lower = np.array([0, 0, 0], dtype=np.uint8)
#        self.upper = np.array([40, 255, 255], dtype=np.uint8)
        
        self.width = 640
        self.left_lane_point= np.array([]) # np.column_stack([[-100]*5,[0]*5]) # [[x1, y1], ..., [xn, yn]]
        self.right_lane_point = np.array([]) # np.column_stack([[740]*5,[0]*5])
        self.left_point_b = []
        self.right_point_b = []
        self.vis_flag = vis_flag
        self.LookoutRange = LookoutRange
        self.Region_WB = Region_WB
        self.avg_a = 128
        self.avg_b = 128
        self.a_fit_left = [0, 220]
        self.a_fit_right = [0, 420]
        self.fit_point_middle = 320
        self.fit_function_left = []
        self.fit_function_right = []
        self.fit_function_middle = []
        self.fit_point_left = []
        self.fit_point_right = []
        self.fit_point_left_b = []
        self.fit_point_right_b = []
        self.frame_WB = []
        self.slice_binary = []
        self.slice_hsv = []
        self.slice_blur = []
        self.slice_hue = []
        self.left_turn_count = [0]*6
        self.right_turn_count = [0]*6
        self.waypoint_turn_b = [5, 0]
        self.Region_lane = [290, 310, 190, 200] #[300,310,250,260]
        self.R_lane = 150
        self.G_lane = 150
        self.B_lane = 150
        self.FirstRun = True
        self.left_turn = False
        self.right_turn = False
        self.fit_point_right_old = np.array([[2,0],[3,0]])

    def white_balance_ini(self):
#        result = cv2.cvtColor(self.frame, cv2.COLOR_BGR2LAB)
#        x_min, x_max, y_min, y_max = self.Region_WB
#        self.avg_a = np.average(result[y_min:y_max, x_min:x_max, 1]) 
#        self.avg_b = np.average(result[y_min:y_max, x_min:x_max, 2]) 
        x_min, x_max, y_min, y_max = self.Region_WB
        B_WB = np.average(self.frame[y_min:y_max, x_min:x_max, 0])
        G_WB = np.average(self.frame[y_min:y_max, x_min:x_max, 1])
        R_WB = np.average(self.frame[y_min:y_max, x_min:x_max, 2])
        color_avg = B_WB/3 + G_WB/3 + R_WB/3

        self.B_ratio = (B_WB-color_avg)/color_avg*0.5 + 1 #0.5
        self.G_ratio = (G_WB-color_avg)/color_avg*0.5 + 1
        self.R_ratio = (R_WB-color_avg)/color_avg*0.5 + 1
#        print("B",self.B_ratio)
#        print("G",self.G_ratio)
#        print("R",self.R_ratio)
        
    def white_balance(self, img): 
#        result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
#        result[:, :, 1] = result[:, :, 1] - ((self.avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1) # *1.1 overshoot
#        result[:, :, 2] = result[:, :, 2] - ((self.avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1) # *1.1 overshoot
#        result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
        result = img
        result[:, :, 0] = result[:, :, 0]/self.B_ratio 
        result[:, :, 1] = result[:, :, 1]/self.G_ratio
        result[:, :, 2] = result[:, :, 2]/self.R_ratio
        return result
    def lane_color(self):
        x_min, x_max, y_min, y_max = self.Region_lane
        area = (x_max-x_min)*(y_max-y_min)
        self.B_lane = np.sum(self.frame[y_min:y_max, x_min:x_max, 0]/area)
        self.G_lane = np.sum(self.frame[y_min:y_max, x_min:x_max, 1]/area)
        self.R_lane = np.sum(self.frame[y_min:y_max, x_min:x_max, 2]/area)
        
    def detect_yellow(self,sliced_frame, center):

        #self.white_balance_ini()    
        #sliced_frame = self.white_balance(sliced_frame)

        slice_blur = cv2.GaussianBlur(sliced_frame,(9,9),0)
        sliced_frame = slice_blur
        
#        hsv = cv2.cvtColor(sliced_frame, cv2.COLOR_BGR2HSV)
##        hue = hsv[:,:,0]
#        mask_threshold = cv2.inRange(hsv, self.lower, self.upper)

        B, G, R = sliced_frame[:,:,0], sliced_frame[:,:,1], sliced_frame[:,:,2]
#        mask_1 = cv2.inRange(R-B, 10, 100) # R>B
#        
#        mask_2 = cv2.inRange(G-B, 15, 100) # G>B
        
        scale = 1
        delta = 0
        ddepth = cv2.CV_16S
        gray = cv2.cvtColor(sliced_frame, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
        grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
        laplacian = cv2.Laplacian(gray,cv2.CV_64F)
        
        sobelx = cv2.convertScaleAbs(grad_x)
        sobely = cv2.convertScaleAbs(grad_y)
        laplacian = cv2.convertScaleAbs(laplacian)
        grad = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)
    
        ret, mask_1 = cv2.threshold(grad,50,255,cv2.THRESH_BINARY) #200
        #mean = B/3 + G/3 + R/3
        #mask_3 = cv2.inRange(mean, 190, 225)
        #mask_3 = cv2.inRange(R, 170, 255)
        
#        std1 = np.sqrt( (B-mean)**2 + (G-mean)**2 + (R-mean)**2 )#/mean 
#        std2 = np.sqrt( (B-self.B_lane)**2 + (G-self.G_lane)**2 + (R-self.R_lane)**2 )
        mask_threshold_lane1 = cv2.inRange(G, self.G_lane, 255)
#        print("G_lane",self.G_lane)
#        print("R_lane",self.R_lane)
        mask_threshold_lane2 = cv2.inRange(R, self.R_lane, 255)
#        mask_threshold_shade_B = cv2.inRange(B,80,255)
#        mask_threshold_shade_R = cv2.inRange(R,0,90)
        
#        mask = mask_threshold_lane1 & mask_threshold_lane2 & (~(mask_threshold_shade_B & mask_threshold_shade_R)) #mask_threshold 
        mask = mask_1 & mask_threshold_lane1 & mask_threshold_lane2 #& mask_3
        #mask = 
        
         #
#        mask = mask_threshold
#        mask = mask_threshold_lane2

#        self.frame_canny = cv2.Canny(mask, 15, 15)
#        lines = cv2.HoughLines(mask,1,np.pi/180,50)
#        try:
#            for rho,theta in lines[0]:
#                a = np.cos(theta)
#                b = np.sin(theta)
#                x0 = a*rho
#                y0 = b*rho
#                x1 = int(x0 + 1000*(-b))
#                y1 = int(y0 + 1000*(a))
#                x2 = int(x0 - 1000*(-b))
#                y2 = int(y0 - 1000*(a))
#            cv2.line(slice_blur, (x1,y1), (x2,y2), (0,0,255), 2)     
#        except:
#            pass

        
        left_point = -100
        right_point = 740
        scan_len = 20
            
            
        for j in range(center, self.width, 5): # int(len(mask)/2)
            try:
                patch = mask[:,j-scan_len:j] #int(len(mask)) :2
                count = np.count_nonzero(patch)
                if count > len(mask)*3: #10:
                   right_point = j-scan_len
                   break
            except:
                continue


        return mask,sliced_frame, slice_blur, left_point,right_point


    def run(self):
        #ret, self.frame = self.cap.read()
        self.res1 = True
        self.frame_WB = self.frame # initialize frame_WB
        #if ret == False:
        #    print ("Nothing read in")
        #    return 0        # print (self.frame)
        
#        if self.FirstRun == True:
#            self.lane_color()
#            self.FirstRun = False
        self.lane_color()


#        # Initialize the white balace to get the color bias

#        self.white_balance_ini()    
#        self.frame_WB = self.white_balance(self.frame_WB)
        
        # Calculate the lookout ranges and the corresponding slice_width
        for i in range(self.num):
            x, self.Ym[i] = CamBodyConversion.BodyToCam_pt([self.LookoutRange[i], 0])
        # parallel to compute lines
        slice_array = []
        for i in range(self.num -1):
            
            slice_array.append(self.frame_WB[self.Ym[i+1]:self.Ym[i],:,:])
        slice_array.append(self.frame_WB[self.Ym[self.num-1]-int((self.Ym[self.num-2]-self.Ym[self.num-1])/1):self.Ym[self.num-1],:,:])
        #[self.frame[self.Y1m:self.Y1m+self.slice_width,:,:],self.frame[self.Y2m:self.Y2m+self.slice_width,:,:],self.frame[self.Y3m:self.Y3m+self.slice_width,:,:]]
        # pool = multiprocessing.Pool(processes=3)
        # result_list = pool.map(self.detect_yellow, slice_array)
        result_list = [-1]*self.num
        for i in range(self.num):
            # Calcute the center for line detection by using the previous middle line function
            center = self.fit_point_middle #320 #int(self.a_fit_middle[0] * self.Ym[i] + self.a_fit_middle[1]) 
#            print('center:', center)
            result_list[i] = self.detect_yellow(slice_array[i], center)
            
        left_point, right_point = [-100]*self.num, [740]*self.num
        self.slice_binary = []
        self.slice_blur = []
#        self.slice_hue = []
        for i in range(self.num):
            mask, sliced_frame, slice_blur, left_point[i],right_point[i] = result_list[i]
            self.mask_array[i] = mask
            if self.vis_flag:
                # cv2.imshow('frame'+str(i), mask) # sliced_frame
                # cv2.imshow('frame'+str(i)+' edge', edge)
                if self.slice_binary == []:
                    self.slice_binary =  mask
                else:
                    self.slice_binary = np.vstack((mask, self.slice_binary)) 
                if self.slice_blur == []:
                    self.slice_blur =  slice_blur
                else:
                    self.slice_blur = np.vstack((slice_blur, self.slice_blur)) 
#                if self.slice_hue == []:
#                    self.slice_hue =  hue
#                else:
#                    self.slice_hue = np.vstack((hue, self.slice_hue)) 
        
        # Only keep the valid lane points
        self.left_lane_point = np.array([])
        self.right_lane_point = np.array([])
        for i in range(self.num-1):
            if left_point[i] > 0:
                self.left_lane_point = np.append(self.left_lane_point, [left_point[i], int((self.Ym[i] + self.Ym[i+1])/2)])
            if right_point[i] < 640:
                self.right_lane_point = np.append(self.right_lane_point, [right_point[i], int((self.Ym[i] + self.Ym[i+1])/2)])
        if left_point[self.num-1] > 0:
                self.left_lane_point = np.append(self.left_lane_point, [left_point[self.num-1], self.Ym[self.num-1]-int((self.Ym[self.num-2]-self.Ym[self.num-1])/1)])
        if right_point[self.num-1] < 640:
                self.right_lane_point = np.append(self.right_lane_point, [right_point[self.num-1], self.Ym[self.num-1]-int((self.Ym[self.num-2]-self.Ym[self.num-1])/1)])
        self.left_lane_point = np.reshape(self.left_lane_point,(-1,2))
        self.right_lane_point = np.reshape(self.right_lane_point,(-1,2))
        
        # Filter the lane points
        
        
        # Convert the lane points to the body frame
        left_point = np.transpose(self.left_lane_point)
        right_point = np.transpose(self.right_lane_point)
        self.left_point_b, self.right_point_b = CamBodyConversion.CamToBody(left_point,right_point)
        self.left_point_b = np.array(self.left_point_b)
        self.right_point_b = np.array(self.right_point_b)

        
        # Remove outliers
        
        if len(self.right_point_b.shape) > 1:
            # Calculate the linear regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(self.right_point_b[:,0],self.right_point_b[:,1])
            # Set stack for the points closed to the regression line
            right_filter = np.array([])
            # Start to check if it is closed to the line for each point
            for i in range(len(self.right_point_b)):
                # The distance of the points to the regression linear
                x, y = self.right_point_b[i,0], self.right_point_b[i,1]
                d = abs(y - x*slope - intercept)/np.sqrt(slope*slope+1)
                # If closed enough to the line
                if d < 0.05:
                    if len(right_filter) > 0:
                        right_filter = np.vstack((right_filter, self.right_lane_point[i]))
                    else:
                        right_filter = self.right_lane_point[i]
            # Replace the original lane points by the stack
            self.right_lane_point = right_filter


        # Line fitting
        self.fitting()
        
#        self.left_turn, self.right_turn = self.turn()
#        # waypoint at turn
#        self.waypoint_turn_b = [5, 0]
#        if self.left_turn == True:
#            if len(self.left_point_b.shape) > 1:
#                for i in range(len(self.left_point_b)):
#                    if self.waypoint_turn_b[1] > self.left_point_b[i][1]:
#                       self.waypoint_turn_b = self.left_point_b[i] + [0.65, 0.25]

#        if self.right_turn == True:
#            if len(self.right_point_b.shape) > 1:
#                for i in range(len(self.right_point_b)):
#                    if self.waypoint_turn_b[1] > self.right_point_b[i][1]:
#                       self.waypoint_turn_b = self.right_point_b[i] + [0.65, -0.25]

        
        
    def fitting(self):

#        self.fit_point_left = []
#        self.fit_point_right = []
#        self.fit_point_left_b = []
#        self.fit_point_right_b = []
        
        n_left = self.left_lane_point.shape[0]
        n_right = self.right_lane_point.shape[0]
        
          # Calculate fitting Coefficients:

            
        if  n_right >= 2 and len(self.right_lane_point.shape) > 1:
            self.fit_point_left = []
            self.fit_point_right = []
            if n_right == 2:
                degree_fit_right = 1
            elif n_right == 3:
                degree_fit_right = 1
            else:
                degree_fit_right = 1
            self.a_fit_right = np.polyfit(self.right_lane_point[:,1], self.right_lane_point[:,0], degree_fit_right)
            # Fitting function:
            self.fit_function_right = np.poly1d(self.a_fit_right)
            # Fitting points:
            for i in range(self.Ym[self.num-1], int(self.right_lane_point[0,1]), 10): #int(self.right_lane_point[-1,1])
                if int(self.fit_function_right(i)) > 640:
                    pass
                else:
                    self.fit_point_right = np.append(self.fit_point_right, [int(self.fit_function_right(i)),i])
            self.fit_point_right = np.reshape(self.fit_point_right,(-1,2))
            self.fit_point_right = self.fit_point_right.astype(int)
            # Convert the fitting points to the body frame
            self.fit_point_right_b = CamBodyConversion.CamToBody_pt(self.fit_point_right[0])
            self.fit_point_right_old = self.fit_point_right
        else: 
            self.fit_point_right = self.fit_point_right_old
                
        "Added for single yellowline"
        #print("right", self.fit_point_right_b)
        if len(self.fit_point_right_b) > 1:
            self.fit_point_left_b = [self.fit_point_right_b[0], self.fit_point_right_b[1] - 1]
        else:
            self.fit_point_left_b = []
        #print("left", self.fit_point_left_b)
        


        # Set the center point based on the right line
#        if len(self.fit_point_right) >= 2:
#            self.fit_point_middle = CamBodyConversion.BodyToCam_pt([self.fit_point_right_b[0], self.fit_point_right_b[1] - 1])
#            print(self.fit_point_middle)
#            self.fit_point_middle = self.fit_point_middle[1]
#            
#        else:
        self.fit_point_middle = 320

    def turn(self):
        
        if len(self.a_fit_left) >= 3:
            if any(abs(self.a_fit_left[:-2]) > 0.4):
                #cv2.putText(self.frame_WB, 'left turn!' , (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
#                left_turn = True
                self.left_turn_count = self.left_turn_count[1:]
                self.left_turn_count.append(1)

            else:
                #cv2.putText(self.frame_WB, 'No left turn!' , (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
                #left_turn = False
                self.left_turn_count = self.left_turn_count[1:]
                self.left_turn_count.append(0)
        else:
            #cv2.putText(self.frame_WB, 'No left turn!' , (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
            #left_turn = False
            self.left_turn_count = self.left_turn_count[1:]
            self.left_turn_count.append(0)
            
        
        if len(self.a_fit_right) >= 3:
            if any(abs(self.a_fit_right[:-2]) > 0.4):
                #cv2.putText(self.frame_WB, 'right turn!' , (400, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
                #right_turn = True
                self.right_turn_count = self.right_turn_count[1:]
                self.right_turn_count.append(1)
                self.res[3] = True
                self.res[4] = True
            else:
                #cv2.putText(self.frame_WB, 'No right turn!' , (400, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
                #right_turn = False
                self.right_turn_count = self.right_turn_count[1:]
                self.right_turn_count.append(0)
        else:
            #cv2.putText(self.frame_WB, 'No right turn!' , (400, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
            #right_turn = False
            self.right_turn_count = self.right_turn_count[1:]
            self.right_turn_count.append(0)
        
        if np.sum(self.left_turn_count) > 1:
            left_turn = True
            self.res4 = True
            self.res5 = False
            cv2.putText(self.frame_WB, 'left turn!' , (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
        else:
            left_turn = False
            cv2.putText(self.frame_WB, 'No left turn!' , (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
            
        if np.sum(self.right_turn_count) > 1:
            right_turn = True
            self.res4 = True
            self.res5 = False
            cv2.putText(self.frame_WB, 'right turn!' , (400, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
        else:
            right_turn = False
            cv2.putText(self.frame_WB, 'No right turn!' , (400, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
            
#        print('self.right_turn_count',self.right_turn_count)
#        print(len(self.a_fit_right))
#        print(self.a_fit_right[:-2])
        # print("left coefficient: ", self.a_fit_left)
        return left_turn, right_turn
        
    def draw(self):
            # Draw lane points, lines and print the position
        #self.frame_WB = self.white_balance(self.frame)

        try:    
            cv2.polylines(self.frame_WB, [self.fit_point_left], False, (255,0,0),3)
        except: 
            pass
        try:    
            cv2.polylines(self.frame_WB, [self.fit_point_right], False, (255,0,0),3)
        except:
            pass


        try:
            for i in range(len(self.left_lane_point)):
                row_left, col = int(self.left_lane_point[i][0]), int(self.left_lane_point[i][1])
                cv2.circle(self.frame_WB,(row_left, col), 5, (0,255,0), -1)
                cv2.putText(self.frame_WB,str([round(self.left_point_b[i][0],1),round(self.left_point_b[i][1],1)]), (row_left, col), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
                self.res2 = True
        except:
            pass
        try:
            for i in range(len(self.right_lane_point)):
                row_right, col = int(self.right_lane_point[i][0]), int(self.right_lane_point[i][1])
                cv2.circle(self.frame_WB,(row_right, col), 5, (0,255,0), -1) # thickness = -1 for a filled circle 
                cv2.putText(self.frame_WB,str([round(self.right_point_b[i][0],1),round(self.right_point_b[i][1],1)]), (row_right, col), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
                self.res3 = True
        except:
            pass        
        
        # Mark the nominal region for white balance
        cv2.rectangle(self.frame_WB, (self.Region_WB[0],self.Region_WB[2]), (self.Region_WB[1],self.Region_WB[3]), (255,0,255))

        
        # Draw the region of interest
        cv2.line(self.frame_WB, (0,self.Ym[0]), (640,self.Ym[0]), (255,0,255))
        cv2.line(self.frame_WB, (0,2*self.Ym[self.num-1]-self.Ym[self.num-2]), (640,2*self.Ym[self.num-1]-self.Ym[self.num-2]), (255,0,255))
        
	
    def line_detec(self,image):
        self.LookoutRange = LookoutRange = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5.5, 6.5, 7.5] #[1.5, 2.5, 3.5, 5, 7]# 
        self.Region_WB = Region_WB = [250, 270, 360, 380]
        self.frame = image.frame
        self.run()
        self.draw()
        slice_binary_rgb = cv2.cvtColor(self.slice_binary, cv2.COLOR_GRAY2BGR)
        frame_comparison = np.vstack((self.frame_WB, self.slice_blur))
        frame_comparison = np.vstack((frame_comparison, slice_binary_rgb))
        return frame_comparison,self.res1,self.res1,self.res1,self.res1,self.res1











