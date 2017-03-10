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
parser.add_argument('-p', "--preview", action='store_false', help="toggle preview")
parser.add_argument('-f', "--flip", action='store_false', help="flip the frame vertically")
parser.add_argument('-s', "--space", action='store_true', help="add a space between every two characters")
parser.add_argument('-w', "--width", type=int, default=64, help="specify the width of the output")
parser.add_argument('-fps', "--framerate", type=int, default=12, help="specify the frames per second")
parser.add_argument('-v', "--video", help="path to the video file")
parser.add_argument('-i', "--image", help="path to the image file")
parser.add_argument('-o', "--out", default="out.man", help="path to the ouput file")
args = parser.parse_args()

# comment out the list you like or even define your own character list
char_list = ["龘","驫","羴","掱","蟲","淼","品","壵","尛","太","大","木","乂","人","丿","丶"] # 16-bit char list
#char_list = ["龘","驫","羴","淼","壵","从","人","一"] # 8-bit char list
#char_list = ["龘","淼","从","人"] # 4-bit char list
#char_list = ["W","N","Z","?","!",";","."," "] # 8-bit non-chinese char list

if args.image:
    # open the file to write
    print "opening the text file..."
    file = open(args.out, 'w')

    # read image file as grayscale
    print "loading the image file..."
    img = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)

    # get the height and width of the image
    height, width = img.shape

    # resize the image
    img = cv2.resize(img,(args.width, height*args.width/width), interpolation = cv2.INTER_CUBIC)

    # get the new height and width of the image
    height, width = img.shape

    # loop through each row of pixels
    print "converting..."

    contentToWrite = ""
    for i in range(height):

        # loop through each pixel in the i-th row
        for j in range(width):

            # write corresponding chinese characters based on the color of the pixel
            char_length = len(char_list)
            for k in range(char_length):
                if img[i, j] < 256/char_length*(k+1) and img[i, j] >= 256/char_length*k:
                    if args.reverse:
                        contentToWrite += char_list[char_length-k-1]
                    else:
                        contentToWrite += char_list[k]
                    if args.space:
                        contentToWrite += ' '
                    break

        # write a new line
        contentToWrite += "\n"

    if args.preview:
        print contentToWrite

    print "saving file..."
    file.write(contentToWrite)
    # close file
    print "closing file..."
    file.close()
    print "done!"
    sys.exit()

# turn on webcam when video file is not specified
if args.video:
    videoSource = args.video
else:
    videoSource = 0

# initialize video capture from builtin webcam
cap = cv2.VideoCapture(videoSource)

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
    file.write(str(args.width)+",")
    file.write(str(image_height)+",")
    file.write(str(args.framerate)+"\n")

    if not args.preview:
        print "recording..."

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

        if args.preview:
            # clear the terminal window
            print(chr(27) + "[2J")

            # print out the frame
            print frameToPrint
        file.write(frameToPrint)

        # when preview on or webcam mode, that is, no delay if converting video with preview off
        if args.preview or args.video:
            # define the period of time each frame's gonna last
            time.sleep(1.0/args.framerate)

# handle KeyboardInterrupt, typically Ctrl + C
except KeyboardInterrupt:
    # release the video capture
    file.close()
    cap.release()
    sys.exit()