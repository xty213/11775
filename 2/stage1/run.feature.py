#!/usr/bin/env python
import os

baseDir = '/data/MM2/MED/MED11/dev/features/sift/sift_ColorSIFTSpbof_ColorSIFTMerge/video/MED10/'
outDir = '/home/tianyux/hw2_stage1/features/'

files = os.listdir(baseDir)
for filename in files:
    inFile = open(baseDir + filename, 'r')
    feature = None
    for line in inFile:
        feature = map(lambda str:str.split(':')[1], line.strip().split(' '))
    inFile.close()

    outFile = open(outDir + filename.split('.')[0] + '.sift.csv', 'w+')
    outFile.write(';'.join(feature))
    outFile.close()
