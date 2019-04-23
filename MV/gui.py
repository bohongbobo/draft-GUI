#----------------------------------------------#
# Autonomous Vehicle Machine Vision System     #
# Graphical User Interface                     #
# gui.py                                       #
# Written by:                                  #
# Jeremy Beauchamp, Zhaojie Chen,              #
# Trenton Davis, and Xudong Yuan               #
#----------------------------------------------#

'''
This file contains the GUI class, which allows the video captured by the camera
to be displayed on the screen. This will primarily be used for testing purposes.
'''

# Import libraries
import tkinter as tk
import cv2
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox as MB
import os
from tkinter import scrolledtext
import sys
from tkinter import BOTH, END, LEFT, RIGHT
import statemachine as SM

#GUI Class
################################################################################
class printout():
    def write(self, s):
        #lbtext.config(state=NORMAL)
        lbtext.insert(END, s)
        #lbtext.config(state=DISABLED)
        lbtext.see(END)
    def flush(self):
        pass

class printin():
    def write(self, s):
        lbtext.insert(END, s)

    def flush(self):
        pass

class GUI:
	'''
	The GUI class contains all of the functionality required to make and operate
	a GUI for the Machine Vision System.

	:ivar root: the window displayed on the screen
	:ivar canvas: the section of the window set aside
	:ivar active: indicates if the window is open or not
	'''

	def __init__(self, title = ""):
            '''
            The constructor for the GUI class. This initializes Tkinter.

            :type title: string
            :param title: the title of the window
            '''

            self.root = tk.Toplevel()
            self.root.title = title
            #self.idle = tk.Label(self.root, text = "Loading...")
            #self.idle.pack()
            self.active = False

            # If window is closed call deactivate function
            self.root.protocol("WM_DELETE_WINDOW", self.deactivate)

            self.quitbtn = tk.Button(self.root, text="Quit", width=12, command=self.quit_btn)
            self.quitbtn.pack()
            global lbtext
            lbtext = scrolledtext.ScrolledText(self.root)
            lbtext.pack(side=RIGHT, ipady=180)
            lbtext1 = scrolledtext.ScrolledText(self.root)
            lbtext1.pack()

            #self.sm = SM.StateMachine('')

#            out = self.sm.current_state
#            self.lbtext1.insert(END, out)


	def quit_btn(self):
		self.root.destroy()

	def activate(self):
		'''
		Creates canvas to display images.
		'''

		#self.idle.destroy()
		self.canvas = tk.Canvas(self.root, height = 720, width = 1280)
		self.canvas.pack()
		self.root.protocol("WM_DELETE_WINDOW", self.deactivate)
		self.active = True


	def deactivate(self):
		'''
		Destroys window.
		'''

		self.root.destroy()
		self.active = False


	def display(self, image):
		'''
		Gets an imageData object, converts it to Tkinter format, and displays it.

		:type image: ImageData object:
		:param image: the image to be displayed
		'''

		# Converts images from OpenCV format to Tkinter's PhotoImage format
		frame = image.frame
		frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		frame2 = Image.fromarray(frame1)
		photo = ImageTk.PhotoImage(frame2)

		# Displays image in the window
		self.canvas.create_image(0, 0, image = photo, anchor = tk.NW)
		self.root.update()

################################################################################
