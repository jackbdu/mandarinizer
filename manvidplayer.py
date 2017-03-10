#!/usr/bin/env python
# encoding=utf-8

import time # sleep
import sys  # exit

__author__ = "Jack B. Du"
__copyright__ = "Copyright (c) 2017, Jack B. Du"
__license__ = "MIT"
__email__ = "jackbdu@nyu.edu"

# define the output file name here
filename = "output.manvid"

frames = []
def load_file(filename, frames_to_return):
    try:
        manvidfile = open(filename, "r")
    except IOError:
        print "no such file or directory: " + filename
        sys.exit()

    filetype, image_height = manvidfile.readline().split(',')

    while manvidfile:
        print("get")
        frame = ""
        line = manvidfile.readline()
        if line == "":
            break
        for i in range(int(image_height)-1):
            frame += line
            line = manvidfile.readline()
        frame += line
        frames_to_return.append(frame)

    manvidfile.close()

load_file("output.manvid", frames)

try:
    while True:
        for frame in frames:
            print "1"
            # clear the terminal window
            print(chr(27) + "[2J")
            # print the frame
            print frame
            time.sleep(0.2)

# handle KeyboardInterrupt, typically Ctrl + C
except KeyboardInterrupt:
    sys.exit()
