#!/bin/bash

# An example script for multimedia event detection (MED) of Homework 1
# Before running this script, you are supposed to have the features by running run.feature.sh 

# Note that this script gives you the very basic setup. Its configuration is by no means the optimal. 
# This is NOT the only solution by which you approach the problem. We highly encourage you to create
# your own setups. For example, any classification algorithms/implementations can be used in your setups.

# Paths to different tools; 
opensmile_path=/data/ASR1/tools/openSmile/bin
speech_tools_path=/home/ymiao/install/speech_tools/bin
ffmpeg_path=/data/ASR1/tools/ffmpeg-2.2.4
export PATH=$opensmile_path:$speech_tools_path:$ffmpeg_path:$PATH
export LD_LIBRARY_PATH=/data/ASR1/tools/ffmpeg-2.2.4/libs:/data/ASR1/tools/openSmile/lib:$LD_LIBRARY_PATH

# Path to python. The sklearn package will be used for k-means clustering
export PATH=/data/ASR1/tools/python27/bin:$PATH
export PYTHONPATH=/data/ASR1/tools/theanoenv/lib/python2.7/site-packages:/home/ymiao/.local/lib/python2.7/site-packages:$PYTHONPATH
export LD_LIBRARY_PATH=/data/ASR1/tools/theanoenv/lib:$LD_LIBRARY_PATH

echo "#####################################"
echo "#          MFCC Features            #"
echo "#####################################"
mkdir -p mfcc_med
# iterate over the events
for event in P001 P002 P003; do
  echo "=========  Event $event  ========="
  # now train a svm model using the sklearn package
  python scripts/train_svm.py $event "kmeans/" 1000 mfcc_med/svm.$event.model || exit 1;
  # apply the svm model to *ALL* the testing videos;
  # output the score of each testing video to a file ${event}_pred 
  python scripts/test_svm.py mfcc_med/svm.$event.model "kmeans/" 1000 mfcc_med/${event}_pred || exit 1;
  # compute the average precision by calling the mAP package
  /data/MM22/xiaojun/Zhigang/mAP/ap ${event}_test_label mfcc_med/${event}_pred
done

echo ""
echo "#####################################"
echo "#           ASR Features            #"
echo "#####################################"
mkdir -p asr_med
# iterate over the events
for event in P001 P002 P003; do
  echo "=========  Event $event  ========="
  # now train a svm model using the sklearn package
  python scripts/train_svm.py $event "asrfeat/" 983 asr_med/svm.$event.model || exit 1;
  # apply the svm model to *ALL* the testing videos;
  # output the score of each testing video to a file ${event}_pred 
  python scripts/test_svm.py asr_med/svm.$event.model "asrfeat/" 983 asr_med/${event}_pred || exit 1;
  # compute the average precision by calling the mAP package
  /data/MM22/xiaojun/Zhigang/mAP/ap ${event}_test_label asr_med/${event}_pred
done

echo ""
echo "#####################################"
echo "#        MFCC+ASR Features          #"
echo "#####################################"
mkdir -p combo_med
# iterate over the events
for event in P001 P002 P003; do
  echo "=========  Event $event  ========="
  # now train a svm model using the sklearn package
  python scripts/train_svm.py $event "combofeat/" 1983 combo_med/svm.$event.model || exit 1;
  # apply the svm model to *ALL* the testing videos;
  # output the score of each testing video to a file ${event}_pred 
  python scripts/test_svm.py combo_med/svm.$event.model "combofeat/" 4983 combo_med/${event}_pred || exit 1;
  # compute the average precision by calling the mAP package
  /data/MM22/xiaojun/Zhigang/mAP/ap ${event}_test_label combo_med/${event}_pred
done
