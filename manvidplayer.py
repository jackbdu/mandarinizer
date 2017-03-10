#!/usr/bin/env python
# encoding=utf-8

import time     # sleep
import sys      # exit
import argparse # argparse

__author__ = 'Jack B. Du'
__copyright__ = 'Copyright (c) 2017, Jack B. Du'
__license__ = 'MIT'
__email__ = 'jackbdu@nyu.edu'

parser = argparse.ArgumentParser()
parser.add_argument('filename', metavar='filename', type=str)
args = parser.parse_args()

framesBuffer = []

def loadFile(filename):
    frames = []
    try:
        manvidfile = open(filename, 'r')
    except IOError:
        print 'no such file or directory: ' + filename
        sys.exit()

    filetype, frameWidthStr, frameHeightStr = manvidfile.readline().split(',')

    while manvidfile:
        frame = ''
        line = manvidfile.readline()
        if line == '':
            break
        for i in range(int(frameHeightStr)-1):
            frame += line
            line = manvidfile.readline()
        frame += line
        frames.append(frame)

    manvidfile.close()

    return frames, int(frameWidthStr), int(frameHeightStr)

print 'loading...'
framesBuffer, frameWidth, frameHeight = loadFile(args.filename)
framesLength = len(framesBuffer)
try:
    while True:
        for i in range(framesLength):
            # clear the terminal window
            print(chr(27) + '[2J')
            # print the frame
            print framesBuffer[i]
            print frameWidth*i/framesLength*'田'+(frameWidth-frameWidth*i/framesLength)*'囗'
            time.sleep(0.2)

# handle KeyboardInterrupt, typically Ctrl + C
except KeyboardInterrupt:
    print frameWidth
    print framesLength
    sys.exit()
