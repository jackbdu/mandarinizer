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

frames = []
def loadFile(filename, frames):
    try:
        manvidfile = open(filename, 'r')
    except IOError:
        print 'no such file or directory: ' + filename
        sys.exit()

    filetype, imageHeight = manvidfile.readline().split(',')

    while manvidfile:
        print('get')
        frame = ''
        line = manvidfile.readline()
        if line == '':
            break
        for i in range(int(imageHeight)-1):
            frame += line
            line = manvidfile.readline()
        frame += line
        frames.append(frame)

    manvidfile.close()

print 'loading file: '+args.filename
loadFile(args.filename, frames)

try:
    while True:
        for frame in frames:
            print '1'
            # clear the terminal window
            print(chr(27) + '[2J')
            # print the frame
            print frame
            time.sleep(0.2)

# handle KeyboardInterrupt, typically Ctrl + C
except KeyboardInterrupt:
    sys.exit()
