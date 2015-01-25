#!/usr/bin/env python
import sys

def writeFile(posEvent, negEvent, eventNum):
    with open(LIST_PATH + 'train_%d.list' % eventNum, 'w+') as f:
        for i in xrange(10):
            f.write('%s,1\n' % posEvent[i])
        for i in xrange((eventNum - 1) * 200, eventNum * 200 - 100):
            f.write('%s,0\n' % negEvent[i])

    with open(LIST_PATH + 'test_%d.list' % eventNum, 'w+') as f:
        for i in xrange(10, len(posEvent)):
            f.write('%s,1\n' % posEvent[i])
        for i in xrange(eventNum * 200 - 100, eventNum * 200):
            f.write('%s,0\n' % negEvent[i])


CSV_PATH = sys.argv[1]
LIST_PATH = sys.argv[2]

posEvent1 = []
posEvent2 = []
posEvent3 = []
negEvent = []

with open(CSV_PATH, 'r') as f:
    for line in f:
        # split each field
        strArr = line.split(',')

        clipID = strArr[0][1:-1]
        eventID = strArr[1][1:-1]
        instType = strArr[2][1:-1]

        if (eventID == 'P001' and instType == 'positive'):
            posEvent1.append(clipID)
        elif (eventID == 'P002' and instType == 'positive'):
            posEvent2.append(clipID)
        elif (eventID == 'P003' and instType == 'positive'):
            posEvent3.append(clipID)
        elif (instType == 'NULL'):
            negEvent.append(clipID)

writeFile(posEvent1, negEvent, 1)
writeFile(posEvent2, negEvent, 2)
writeFile(posEvent3, negEvent, 3)