import sys, os

clusterNum = int(sys.argv[1])
kmeansPath = "/kmeans/%d" % clusterNum

for eventNum in [1, 2, 3]:
    for eventType in ["train", "test"]:
        fileList = open("/list/%s_%d.list" % (eventType, eventNum), 'r')
        outputFile = open("/bow_mfcc/%s_%d.csv" % (eventType, eventNum), 'w+')
        # print table head
        for clusterId in xrange(clusterNum):
            outputFile.write('"cluster%d",' % clusterId)
        outputFile.write('"classLabel"\n')
        try:
            for clipIdAndLabel in fileList:
                clipId = clipIdAndLabel.split(",")[0]
                label = clipIdAndLabel.split(",")[1].strip()
                # if the corresponding MFCC cluster feature file exists
                featureFileName = kmeansPath + "/HVC%s.kmeans.csv" % clipId
                if os.path.isfile(featureFileName):
                    # write the MFCC cluster feature and class label
                    featureFile = open(featureFileName, 'r')
                    try:
                        outputFile.write(",".join(featureFile[0].strip().split(";")))
                        outputFile.write(",Y\n" if label == "1" else ",N\n")
                    finally:
                        featureFile.close()
        finally:
            fileList.close()