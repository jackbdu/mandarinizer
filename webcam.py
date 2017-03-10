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
image_width = 64

# OPTIONAL: comment out the list you like or even define your own character list
char_list = ["龘","驫","羴","掱","𣝯","淼","品","壵","尛","太","大","木","乂","人","丿","丶"] # 16-bit char list
#char_list = ["龘","驫","羴","淼","壵","从","人","一"] # 8-bit char list
#char_list = ["龘","淼","从","人"] # 4-bit char list
#char_list = ["W","N","Z","?","!",";","."," "] # 8-bit non-chinese char list

# OPTIONAL: whehter or not to reverse the image
image_reverse = False

# OPTIONAL: whether or not to add a space between characters
add_space = False

# OPTIONAL: whether or not to flip the image vertically
image_flip = True

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

                # flip the image vertically
                if (image_flip):
                    img = cv2.flip(img, 1)

		# get the new height and width of the image
		height, width = img.shape

		# initialize an empty string to store the entire frame of text
		frameToPrint = ""

		# loop through each row of pixels of the image
		for i in range(height):

			# loop through each pixel in the i-th row of the image
			for j in range(width):

				# write corresponding chinese characters based on the color of the pixel
                                char_length = len(char_list)
                                for k in range(char_length):
                                    if img[i, j] < 256/char_length*(k+1) and img[i, j] >= 256/char_length*k:
                                        if image_reverse:
                                            frameToPrint += char_list[char_length-k-1]
                                        else:
                                            frameToPrint += char_list[k]
                                        if add_space:
                                            frameToPrint += ' '
                                        break

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
