#!/bin/python
import os
import re

file_names = os.listdir('sift_keyframes')
file_names.sort()

curr_video = file_names[0].split('_')[0]
curr_file = open("sift_video/" + curr_video + ".sift", 'w+')

for file_name in file_names:
    # if it's new video, save the previous video
    if file_name.split('_')[0] != curr_video:
        curr_file.close()
        curr_video = file_name.split('_')[0]
        curr_file = open("sift_video/" + curr_video + ".sift", 'w+')

    feature_of_this_frame = []
    f = open('sift_keyframes/' + file_name, 'r')
    for line in f:
        raw_feature_vector = re.sub(r"[\[\];]", "", line.strip()).split(',')
        feature_of_this_frame.append(";".join(map(lambda x:x.strip() ,raw_feature_vector)))
    curr_file.write("\n".join(feature_of_this_frame) + "\n")
    f.close()
    
curr_file.close()
