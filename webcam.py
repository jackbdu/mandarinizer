#!/usr/bin/env python
# encoding=utf-8

# you need to install opencv before running the script import cv2
import cv2
import time	# sleep
import sys	# exit

__author__ = "Jack B. Du"
__copyright__ = "Copyright (c) 2017, Jack B. Du"
__credits__ = ["Richard Lewei Huang", "Shirley Huang"]
__license__ = "MIT"
__email__ = "jackbdu@nyu.edu"

# initialize video capture from builtin webcam
cap = cv2.VideoCapture(0)

# OPTIONAL: define the desired image width (in pixel) here
image_width = 100

try: 
	while True:
		# read frame from web cam
		ret, frame = cap.read()

		# convert frame to grayscale image
		img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# get the height and width of the image
		height, width = img.shape

		# resize the image
		img = cv2.resize(img,(image_width, height*image_width/width), interpolation = cv2.INTER_CUBIC)

		# get the new height and width of the image
		height, width = img.shape

		# initialize an empty string to store the entire frame of text
		frameToPrint = ""

		# loop through each row of pixels of the image
		for i in range(height):

			# loop through each pixel in the i-th row of the image
			for j in range(width):

				# write corresponding chinese characters based on the color of the pixel
				if img[i,j] < 32:
					frameToPrint += "龘"
				elif img[i,j] < 64:
					frameToPrint += "驫"
				elif img[i,j] < 96:
					frameToPrint += "羴"
				elif img[i,j] < 128:
					frameToPrint += "淼"
				elif img[i,j] < 160:
					frameToPrint += "壵"
				elif img[i,j] < 192:
					frameToPrint += "从"
				elif img[i,j] < 224:
					frameToPrint += "人"
				else:
					frameToPrint += "一"

			# write a new line
			frameToPrint += "\n"
		# clear the terminal window
		print(chr(27) + "[2J")

		# print out the frame
		print frameToPrint

		# define the period of time each frame's gonna last
		time.sleep(0.2)

# handle KeyboardInterrupt, typically Ctrl + C
except KeyboardInterrupt:
	# release the video capture
	cap.release()
	sys.exit()
