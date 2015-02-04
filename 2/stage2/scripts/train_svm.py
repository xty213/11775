#!/bin/python 

import numpy
import os
from sklearn.svm.classes import SVC
from sklearn.metrics.pairwise import chi2_kernel
import cPickle
import sys

# Performs K-means clustering and save the model to a local file

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "Usage: {0} event_name feat_dir feat_dim output_file".format(sys.argv[0])
        print "event_name -- name of the event (P001, P002 or P003 in Homework 1)"
        print "feat_dir -- dir of feature files"
        print "feat_dim -- dim of features"
        print "output_file -- path to save the svm model"
        exit(1)

    event_name = sys.argv[1]
    feat_dir = sys.argv[2]
    feat_dim = int(sys.argv[3])
    output_file = sys.argv[4]

    # assume that you don't change the video list and feature path names
    video_list_file = event_name + '_train'

    # read the list file; get the list of videos and their labels
    # the labels of positive examples are 1 while the labels of the background videos are 0
    video_list = []; label_string = ''
    fopen = open(video_list_file, 'r')
    for line in fopen.readlines():
        splits = line.replace('\n','').split(' ')
        video_list.append(splits[0])
        # the correct class is 1 whereas the background class is 0
        if splits[1] == event_name:
            label_string += '1 '
        else:
            label_string += '0 '
    fopen.close()

    # generate the 
    label_vec = numpy.fromstring(label_string.strip(), dtype=int, sep=' ')
    print 'Totally we get %s labels' % (label_vec.shape[0])  # for debugging

    # create the feature matrix, in which each row represents a video
    video_num = len(video_list)
    feat_mat = numpy.zeros([video_num, feat_dim])
    for i in xrange(video_num):
        # BOW features of this video
        feat_vec = numpy.genfromtxt(feat_dir + video_list[i], dtype=numpy.float32, delimiter=";")
        assert(feat_vec.shape[0] == feat_dim)
        # fill the feature vector to the matrix
        feat_mat[i,:] = feat_vec

    # initialize svm
    svm = SVC(kernel=chi2_kernel)
#    svm = SVC(probability=True)

    # train the svm models
    svm.fit(feat_mat, label_vec) 

    # finally save the k-means model
    cPickle.dump(svm, open(output_file,"wb"), cPickle.HIGHEST_PROTOCOL)

    print 'SVM trained successfully for event %s!' % (event_name)
