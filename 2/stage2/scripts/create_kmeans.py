#!/bin/python
import numpy
import os
import cPickle
from sklearn.cluster.k_means_ import KMeans
import sys
# Generate k-means features for videos; each video is represented by a single vector

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: {0} kmeans_model, cluster_num, file_list".format(sys.argv[0])
        print "kmeans_model -- path to the kmeans model"
        print "cluster_num -- number of cluster"
        print "file_list -- the list of videos"
        exit(1)

    kmeans_model = sys.argv[1]; file_list = sys.argv[3]
    cluster_num = int(sys.argv[2])

    # load the kmeans model
    kmeans = cPickle.load(open(kmeans_model,"rb"))
    
    fread = open(file_list, "r")
    for line in fread.readlines():
        mfcc_path = "sift_video/" + line.replace('\n','') + ".sift"
        fwrite = open('sift_kmeans/' + line.replace('\n',''),'w')
        cluster_histogram = numpy.zeros(cluster_num)

        if os.path.exists(mfcc_path) == True:
            array = numpy.genfromtxt(mfcc_path, delimiter=";")
            pred = kmeans.predict(array)

            # for each video, get the hostogram of the clusters
            # and then normalize the histogram to be a probability distribution
            for x in pred:
                cluster_histogram[x] += 1
            for m in xrange(cluster_num):
                cluster_histogram[m] /= len(pred)
        else:
            cluster_histogram.fill(1.0/cluster_num)  # for videos that have no MFCC features, we simply set all the features to
                                                     # be 1.0/cluster_num

        line = str(cluster_histogram[0])
        for m in range(1, cluster_num):
            line += ';' + str(cluster_histogram[m])
        fwrite.write(line + '\n')
        fwrite.close()

    print "K-means features generated successfully!"
