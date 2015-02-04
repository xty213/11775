#!/bin/python
import numpy
import os
import cPickle
from sklearn.cluster.k_means_ import KMeans
import sys
# Generate ASR-based features for videos; each video is represented by a single vector which has the same dimension
# as the size of the vocabulary

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "Usage: {0} file_list, in_feat1_dir, in_feat2_dir, out_feat_dir".format(sys.argv[0])
        print "file_list -- the list of videos"
        print "in_feat1_dir -- directory of the first feature type (e.g., MFCC)"
        print "in_feat2_dir -- directory of the second feature type (e.g., ASR)"
        print "out_feat_dir -- directory to save the combined features"
        exit(1)

    file_list = sys.argv[1]; in_feat1_dir = sys.argv[2]; in_feat2_dir = sys.argv[3]; out_feat_dir = sys.argv[4]

    fread = open(file_list, "r")
    for line in fread.readlines():
        line = line.replace('\n','')
        fread_tmp = open(in_feat1_dir + '/' + line, 'r')
        feat1 = fread_tmp.readline().replace('\n','')
        fread_tmp.close()
        fread_tmp = open(in_feat2_dir + '/' + line, 'r')
        feat2 = fread_tmp.readline().replace('\n','')
        fread_tmp.close()

        fout = open(out_feat_dir + '/' + line,'w')
        fout.write(feat1 + ';' + feat2 + '\n')
        fout.close()
    print "Combined features generated successfully!"
