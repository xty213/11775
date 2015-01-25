#!/bin/bash

WEKA_PATH='weka/'
FILE_LIST_PATH='list/'
CLIP_LABEL_FILE_PATH=${FILE_LIST_PATH}'MED10TRN_20101215_JudgementMD.csv'
ASR_PATH='asr/'
BOW_PATH='bow/'


./scripts/gen_dataset_list.py $CLIP_LABEL_FILE_PATH $FILE_LIST_PATH
./scripts/get_bag_of_word.py $FILE_LIST_PATH $ASR_PATH $BOW_PATH

for eventNum in 1 2 3
do
    java -cp ${WEKA_PATH}weka.jar weka.classifiers.functions.Logistic -R 1.0E-8 -M -1 -t bow/train_${eventNum}.csv -T bow/test_${eventNum}.csv > result/asr_${eventNum}.out
done