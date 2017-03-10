#!/usr/bin/env python
# encoding=utf-8

# you need to install opencv before running the script import cv2
import sys      # exit
import time     # sleep
import argparse # argparse
import cv2

__author__ = "Jack B. Du"
__copyright__ = "Copyright (c) 2017, Jack B. Du"
__credits__ = ["Richard Lewei Huang", "Shirley Huang"]
__license__ = "MIT"
__email__ = "jackbdu@nyu.edu"

# parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument('-r', "--reverse", action='store_false', help="reverse the color value of the frame")
parser.add_argument('-f', "--flip", action='store_false', help="flip the video vertically")
parser.add_argument('-s', "--space", action='store_true', help="add a space between every two characters")
parser.add_argument('-w', "--width", type=int, default=64, help="specify the width of the output video")
parser.add_argument('-fps', "--framerate", type=int, default=12, help="specify the frames per second")
parser.add_argument('-v', "--video", help="path to the video file")
parser.add_argument('-o', "--out", default="out.manvid", help="path to the ouput file")
args = parser.parse_args()

# turn on webcam when video file is not specified
if args.video:
    videoSource = args.video
else:
    videoSource = 0

# initialize video capture from builtin webcam
cap = cv2.VideoCapture(videoSource)

# OPTIONAL: comment out the list you like or even define your own character list
char_list = ["龘","驫","羴","掱","蟲","淼","品","壵","尛","太","大","木","乂","人","丿","丶"] # 16-bit char list
#char_list = ["龘","驫","羴","淼","壵","从","人","一"] # 8-bit char list
#char_list = ["龘","淼","从","人"] # 4-bit char list
#char_list = ["W","N","Z","?","!",";","."," "] # 8-bit non-chinese char list

try: 
    # open the file to write
    file = open(args.out, "w")
    # write file type in the first line of output file
    file.write("manvid,")

    # read frame from web cam
    ret, frame = cap.read()
    # convert frame to grayscale image
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    # get the height and width of the image
    height, width = img.shape
    # calculate the image height based on the image width
    image_height = height*args.width/width

    # write meta data in the first line of output file
    file.write(str(args.width)+","+str(image_height)+"\n")

    while True:
        # read frame from web cam
        ret, frame = cap.read()

        # convert frame to grayscale image
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # resize the image
        img = cv2.resize(img,(args.width, image_height), interpolation = cv2.INTER_CUBIC)

        # flip the image vertically
        if (args.flip):
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
                        if args.reverse:
                            frameToPrint += char_list[char_length-k-1]
                        else:
                            frameToPrint += char_list[k]
                        if args.space:
                            frameToPrint += ' '
                        break

            # write a new line
            frameToPrint += "\n"
        # clear the terminal window
        print(chr(27) + "[2J")

        # print out the frame
        print frameToPrint
        file.write(frameToPrint)

        # define the period of time each frame's gonna last
        time.sleep(1.0/args.framerate)

# handle KeyboardInterrupt, typically Ctrl + C
except KeyboardInterrupt:
    # release the video capture
    file.close()
    cap.release()
    sys.exit()
