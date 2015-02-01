#!/usr/bin/env python
import os, sys

LIST_PATH = sys.argv[1]
ASR_PATH = sys.argv[2]
BOW_PATH = sys.argv[3]
EVENT_LIST = [1, 2, 3]
STOP_WORD = set("a's,able,about,above,according,accordingly,across,actually,after,afterwards,again,against,ain't,all,allow,allows,almost,alone,along,already,also,although,always,am,among,amongst,an,and,another,any,anybody,anyhow,anyone,anything,anyway,anyways,anywhere,apart,appear,appreciate,appropriate,are,aren't,around,as,aside,ask,asking,associated,at,available,away,awfully,be,became,because,become,becomes,becoming,been,before,beforehand,behind,being,believe,below,beside,besides,best,better,between,beyond,both,brief,but,by,c'mon,c's,came,can,can't,cannot,cant,cause,causes,certain,certainly,changes,clearly,co,com,come,comes,concerning,consequently,consider,considering,contain,containing,contains,corresponding,could,couldn't,course,currently,definitely,described,despite,did,didn't,different,do,does,doesn't,doing,don't,done,down,downwards,during,each,edu,eg,eight,either,else,elsewhere,enough,entirely,especially,et,etc,even,ever,every,everybody,everyone,everything,everywhere,ex,exactly,example,except,far,few,fifth,first,five,followed,following,follows,for,former,formerly,forth,four,from,further,furthermore,get,gets,getting,given,gives,go,goes,going,gone,got,gotten,greetings,had,hadn't,happens,hardly,has,hasn't,have,haven't,having,he,he's,hello,help,hence,her,here,here's,hereafter,hereby,herein,hereupon,hers,herself,hi,him,himself,his,hither,hopefully,how,howbeit,however,i'd,i'll,i'm,i've,ie,if,ignored,immediate,in,inasmuch,inc,indeed,indicate,indicated,indicates,inner,insofar,instead,into,inward,is,isn't,it,it'd,it'll,it's,its,itself,just,keep,keeps,kept,know,knows,known,last,lately,later,latter,latterly,least,less,lest,let,let's,like,liked,likely,little,look,looking,looks,ltd,mainly,many,may,maybe,me,mean,meanwhile,merely,might,more,moreover,most,mostly,much,must,my,myself,name,namely,nd,near,nearly,necessary,need,needs,neither,never,nevertheless,new,next,nine,no,nobody,non,none,noone,nor,normally,not,nothing,novel,now,nowhere,obviously,of,off,often,oh,ok,okay,old,on,once,one,ones,only,onto,or,other,others,otherwise,ought,our,ours,ourselves,out,outside,over,overall,own,particular,particularly,per,perhaps,placed,please,plus,possible,presumably,probably,provides,que,quite,qv,rather,rd,re,really,reasonably,regarding,regardless,regards,relatively,respectively,right,said,same,saw,say,saying,says,second,secondly,see,seeing,seem,seemed,seeming,seems,seen,self,selves,sensible,sent,serious,seriously,seven,several,shall,she,should,shouldn't,since,six,so,some,somebody,somehow,someone,something,sometime,sometimes,somewhat,somewhere,soon,sorry,specified,specify,specifying,still,sub,such,sup,sure,t's,take,taken,tell,tends,th,than,thank,thanks,thanx,that,that's,thats,the,their,theirs,them,themselves,then,thence,there,there's,thereafter,thereby,therefore,therein,theres,thereupon,these,they,they'd,they'll,they're,they've,think,third,this,thorough,thoroughly,those,though,three,through,throughout,thru,thus,to,together,too,took,toward,towards,tried,tries,truly,try,trying,twice,two,un,under,unfortunately,unless,unlikely,until,unto,up,upon,us,use,used,useful,uses,using,usually,value,various,very,via,viz,vs,want,wants,was,wasn't,way,we,we'd,we'll,we're,we've,welcome,well,went,were,weren't,what,what's,whatever,when,whence,whenever,where,where's,whereafter,whereas,whereby,wherein,whereupon,wherever,whether,which,while,whither,who,who's,whoever,whole,whom,whose,why,will,willing,wish,with,within,without,won't,wonder,would,would,wouldn't,yes,yet,you,you'd,you'll,you're,you've,your,yours,yourself,yourselves,zero".split(','))

def writeBoWFile(listPrefix, eventNum, showClipID=False):
    bowFile = open('%s/%s_%d.csv' % (BOW_PATH, listPrefix, eventNum), 'w+')
    try:
        f = open("%s/%s_%d.list" % (LIST_PATH, listPrefix, eventNum), 'r')
        try:
            # print table head
            bowFile.write(",".join(map(lambda x:'"%s"' % x, vocabulary)))
            bowFile.write(',"classLabel"\n')

            for line in f:
                clipID = line.split(',')[0]
                label = line.split(',')[1]
                bow = [0 for i in xrange(len(vocabulary))]
                fileString = "%s/HVC%s.ctm" % (ASR_PATH, clipID)
                if not os.path.exists(fileString):
                    continue
                    
                asr = open(fileString, 'r')
                try:
                    for rec in asr:
                        word = rec.split(" ")[4]
                        if word in vocabulary:
                            bow[voc_map[word]] += 1
                finally:
                    asr.close()

                if showClipID:
                    bowFile.write(clipID + ",")
                bowFile.write(",".join(map(lambda x:str(x), bow)))

                # print class label
                bowFile.write(',class%s' % label)
        finally:
            f.close()
    finally:
        bowFile.close()

def writeTestBoWFile(showClipID=False):
    bowFile = open('%s/test.csv' % BOW_PATH, 'w+')
    try:
        f = open("%s/test.list" % LIST_PATH, 'r')
        try:
            # print table head
            bowFile.write(",".join(map(lambda x:'"%s"' % x, vocabulary)))
            bowFile.write(',"classLabel"\n')

            for line in f:
                clipID = line.split(',')[0]
                label = line.split(',')[1]
                bow = [0 for i in xrange(len(vocabulary))]
                fileString = "%s/HVC%s.ctm" % (ASR_PATH, clipID)
                if not os.path.exists(fileString):
                    continue

                asr = open(fileString, 'r')
                try:
                    for rec in asr:
                        word = rec.split(" ")[4]
                        if word in vocabulary:
                            bow[voc_map[word]] += 1
                finally:
                    asr.close()

                if showClipID:
                    bowFile.write(clipID + ",")
                bowFile.write(",".join(map(lambda x:str(x), bow)))

                # print class label
                bowFile.write(',class%s' % label)
        finally:
            f.close()
    finally:
        bowFile.close()


# read all the training files and get the vocabulary set
vocabulary = set()
for eventNum in EVENT_LIST:
    f = open("%s/train_%d.list" % (LIST_PATH, eventNum), 'r')
    try:
        for line in f:
            clipID = line.split(',')[0]
            fileString = "%s/HVC%s.ctm" % (ASR_PATH, clipID)
            if not os.path.exists(fileString):
                continue
            asr = open(fileString, 'r')
            try:
                for rec in asr:
                    word = rec.split(" ")[4]
                    if word not in STOP_WORD:
                        vocabulary.add(word)
            finally:
                asr.close()
    finally:
        f.close()

# construct bag_of_word representation
voc_map = dict(zip(vocabulary, xrange(len(vocabulary))))
for eventNum in EVENT_LIST:
    writeBoWFile("train", eventNum)
writeTestBoWFile()
