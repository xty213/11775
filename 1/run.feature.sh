#!/bin/bash

# An example script for feature extraction of Homework 1

# Note that this script gives you the very basic setup. Its configuration is by no means the optimal. 
# This is NOT the only solution by which you approach the problem. We highly encourage you to create
# your own setups. For example, any clustering algorithms/implementations can be used in your setups.

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

# Two additional variables
video_path=./video    # path to the directory containing all the videos. In this example setup, we are linking all the videos to "./video"
cluster_num=1000      # the number of clusters in k-means.

mkdir -p audio mfcc kmeans

# This part does feature extraction, it may take quite a while if you have a lot of videos. Totally 3 steps are taken:
# 1. ffmpeg extracts the audio track from each video file into a wav file
# 2. The wav file may contain 2 channels. We always extract the 1st channel using ch_wave
# 3. SMILExtract generates the MFCC features for each wav file
#    The config file MFCC12_0_D_A.conf generates 13-dim MFCCs at each frame, together with the 1st and 2nd deltas. So you 
#    will see each frame totally has 39 dims. 
#    Refer to Section 2.5 of this document http://web.stanford.edu/class/cs224s/hw/openSMILE_manual.pdf for better configuration
#    (e.g., normalization) and other feature types (e.g., PLPs )     
#cat train | awk '{print $1}' > train.video
#cat test | awk '{print $1}' > test.video
#cat train.video test.video > all.video
#for line in $(cat "all.video"); do
#    ffmpeg -y -i $video_path/${line}.mp4 -f wav tmp.wav
#    ch_wave tmp.wav -c 0 -o audio/$line.wav
#    SMILExtract -C config/MFCC12_0_D_A_Z.conf -I audio/$line.wav -O mfcc/$line.mfcc.csv
#done
# You may find the number of MFCC files mfcc/*.mfcc.csv is slightly less than the number of the videos. This is because some of the videos
# don't hae the audio track. For example, HVC1221, HVC1222, HVC1261, HVC1794 

# In this part, we train a clustering model to cluster the MFCC vectors. In order to speed up the clustering process, we
# select a small portion of the MFCC vectors. In the following example, we only select 20% randomly from each video. 
python scripts/select_frames.py train.video 0.2 select.mfcc.csv || exit 1;
# now trains a k-means model using the sklearn package
python scripts/train_kmeans.py select.mfcc.csv $cluster_num kmeans.${cluster_num}.model || exit 1;

# Now that we have the k-means model, we can represent a whole video with the histogram of its MFCC vectors over the clusters. 
# Each video is represented by a single vector which has the same dimension as the number of clusters. 
python scripts/create_kmeans.py kmeans.${cluster_num}.model $cluster_num all.video || exit 1;
# Now you can see that you get the bag-of-word representations under kmeans/. Each video is now represented
# by a 4000-dimensional vector.

# Now we generate the ASR-based features. This requires a vocabulary file to available beforehand. Each video is represented by
# a vector which has the same dimension as the size of the vocabulary. The elements of this vector are the number of occurrences 
# of the corresponding word. The vector is normalized to be like a probability. 
# You can of course explore other better ways, such as TF-IDF, of generating these features.
mkdir -p asrfeat
python scripts/create_asrfeat.py vocab all.video || exit 1;

# We combine the ASR and MFCC features together
mkdir -p combofeat
python scripts/combine_2feats.py all.video kmeans asrfeat combofeat || exit 1;

