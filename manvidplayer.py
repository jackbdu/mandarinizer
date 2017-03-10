#!/usr/bin/env python
# encoding=utf-8

import time     # sleep
import sys      # exit
import argparse # argparse

__author__ = 'Jack B. Du'
__copyright__ = 'Copyright (c) 2017, Jack B. Du'
__license__ = 'MIT'
__email__ = 'jackbdu@nyu.edu'

# parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument('filename', metavar='filename', type=str)
args = parser.parse_args()

# buffer that stores all the frames of texts
framesBuffer = []

# load frames from the file
def load_frames(filename):
    # initialize empty list for frames to return
    frames = []
    try:
        # open file for reading
        manvidfile = open(filename, 'r')
    # error when opening file
    except IOError:
        print 'no such file or directory: ' + filename
        sys.exit()

    # read first line in file
    line = manvidfile.readline()

    # get meta data from the file (first line in the file, seperated by ','
    filetype, frameWidthStr, frameHeightStr = line.split(',')

    # while file not finished
    while line != '':
        # initialize an empty list for storing frame
        frame = ''
        # load one frame
        for i in range(int(frameHeightStr)):
            line = manvidfile.readline()
            # add current line to frame
            frame += line
        # add current frame to frames
        frames.append(frame)

    # close the file
    manvidfile.close()

    return frames, int(frameWidthStr), int(frameHeightStr)

# clear the terminal window
print(chr(27) + '[2J')
print 'loading...'
framesBuffer, frameWidth, frameHeight = load_frames(args.filename)
# get the length (number) of frames
framesLength = len(framesBuffer)

try:
    # repeat frames
    while True:
        # play frames
        for i in range(framesLength):
            # clear the terminal window
            print(chr(27) + '[2J')
            # print the frame
            print framesBuffer[i]
            # progress bar
            print frameWidth*i/framesLength*'田'+(frameWidth-frameWidth*i/framesLength)*'囗'
            # time for one frame
            time.sleep(0.2)

# handle KeyboardInterrupt, typically Ctrl + C
except KeyboardInterrupt:
    sys.exit()
