#!/bin/python
import numpy
import os
import sys
# Convert the features into ARFF

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: {0} set_name, feat_size".format(sys.argv[0])
        print "set_name -- the name of the dataset"
        print "feat_size -- dimension of the features"
        exit(1)

    set_name = sys.argv[1]; feat_size = int(sys.argv[2])

    fwrite = open(set_name + '.arff','w')
    fwrite.write('@relation ' + set_name + '\n')
    for n in xrange(feat_size):
        fwrite.write("@attribute \'F" + str(n) + "\' numeric" + "\n")
    fwrite.write("@attribute \'Type\' { " + set_name + ",NULL }" + "\n")
    fwrite.write("@data\n")

    fread = open(set_name + '.list','r')
    for line in fread.readlines():
        elements = line.replace('\n','').split(' ')
        filename = elements[0]; label = elements[1]
        mfcc_path = "kmeans/" + filename + ".kmeans.csv"
        if os.path.exists(mfcc_path) == False:
            continue
        fdata = open(mfcc_path,'r')
        feat_line = fdata.readline().replace('\n','')
        if feat_line == "":
            continue
        fwrite.write(feat_line.replace(";",',') + ',' + label + "\n")

    fwrite.close()


