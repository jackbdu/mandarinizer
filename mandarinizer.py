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
parser = argparse.ArgumentParser(description="Mandarinize an image file, a video file or a webcam stream.")
parser.add_argument('--version', action='version', version='%(prog)s 0.1') 
parser.add_argument('-inv', "--invert", action='store_true', help="invert the color of the frame")
parser.add_argument('-p', "--preview", action='store_false', help="toggle preview")
parser.add_argument('-f', "--flip", action='store_true', help="toggle the vertical flip of the frame")
parser.add_argument('-s', "--space", action='count', help="add a space between every two characters")
parser.add_argument('-w', "--width", type=int, default=64, help="specify the width of the output")
parser.add_argument('-fps', "--framerate", type=int, default=12, help="specify the frames per second")
parser.add_argument('-d', "--depth", type=int, default=16, choices=[2,4,8,16], help="specify the color depth")
parser.add_argument('-c', "--character", nargs='+', help="specify a list of characters by the order of indensity")
parser.add_argument('-v', "--video", help="path to the video file")
parser.add_argument('-i', "--image", nargs='+', help="paths to the image files")
parser.add_argument('-o', "--out", default="out", help="path to the ouput file")
args = parser.parse_args()

if args.character:
    char_list = args.character
else:
    if args.depth == 2:
        char_list = ["龘","一"] # 2-bit char list
    elif args.depth == 4:
        char_list = ["龘","淼","从","人"] # 4-bit char list
    elif args.depth == 8:
        char_list = ["龘","驫","羴","淼","壵","从","人","一"] # 8-bit char list
    else:
        char_list = ["龘","驫","羴","掱","蟲","淼","品","壵","尛","太","大","木","乂","人","丿","丶"] # 16-bit char list

if args.image:
    for i in range(len(args.image)):
        filename = args.out+'_'+str(i+1)+'.txt';
        # open the file to write
        print "creating the txt file: " + filename
        file = open(filename, 'w')

        # read image file as grayscale
        print "loading the image file: " + args.image[i]
        img = cv2.imread(args.image[i], cv2.IMREAD_GRAYSCALE)

        # get the height and width of the image
        height, width = img.shape

        # resize the image
        img = cv2.resize(img,(args.width, height*args.width/width), interpolation = cv2.INTER_CUBIC)

        # get the new height and width of the image
        height, width = img.shape

        # loop through each row of pixels
        print "mandarinizing..."

        contentToWrite = ""
        for i in range(height):

            # loop through each pixel in the i-th row
            for j in range(width):

                # write corresponding chinese characters based on the color of the pixel
                char_length = len(char_list)
                for k in range(char_length):
                    if img[i, j] < 256/char_length*(k+1) and img[i, j] >= 256/char_length*k:
                        if args.invert:
                            contentToWrite += char_list[char_length-k-1]
                        else:
                            contentToWrite += char_list[k]
                        if args.space:
                            for l in range(args.space):
                                contentToWrite += ' '
                        break

            # write a new line
            contentToWrite += "\n"

        if args.preview:
            print contentToWrite

        print "saving txt file: " + filename
        file.write(contentToWrite)
        # close file
        print "closing txt file: " + filename
        file.close()
        print "mandarinized!"
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
    file = open(args.out+".manvid", "w")
    # write file type in the first line of output file
    file.write("manvid,")

    # read frame from web cam
    ret, frame = cap.read()
    if not ret:
    # release the video capture
        print "video capture failed!"
        file.close()
        cap.release()
        sys.exit()

    # convert frame to grayscale image
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # get the height and width of the image
    height, width = img.shape
    # calculate the image height based on the image width
    image_height = height*args.width/width

    # write meta data in the first line of output file
    file.write(str(args.width)+",")
    file.write(str(image_height)+",")
    file.write(str(args.framerate)+",")
    file.write(str(args.depth)+"\n")

    print "mandarinizing..."

    while True:
        # read frame from web cam
        ret, frame = cap.read()
        if not ret:
            # release the video capture
            print "mandarinized!"
            file.close()
            cap.release()
            sys.exit()

        # preparing the frame for mandarinizing
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.equalizeHist(img)

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
                    if img[i, j] < (k+1)*256/char_length and img[i, j] >= k*256/char_length:
                        if args.invert:
                            frameToPrint += char_list[char_length-k-1]
                        else:
                            frameToPrint += char_list[k]
                        if args.space:
                            for i in range(args.space):
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
