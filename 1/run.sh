#!/bin/bash


###### CONSTANTS ######
# these files must exist before running the pipeline
CLIP_LABEL_FILE_PATH='list/MED10TRN_20101215_JudgementMD.csv'
ASR_PATH='asr'
WEKA_PATH='weka'
SCRIPT_PATH='scripts'
# these folders can be generate automatically
FILE_LIST_PATH='list'
BOW_PATH='bow'
RESULT_PATH='result'
mkdir -p $FILE_LIST_PATH $BOW_PATH $RESULT_PATH


###### PRE_PROCESS ######
echo "Generating training set and test set..."
python ${SCRIPT_PATH}/gen_dataset_list.py $CLIP_LABEL_FILE_PATH $FILE_LIST_PATH


###### ASR TRANSCRIPTION PIPELINE ######
echo "Start ASR transcription pipeline..."
echo "  Generating ASR transcription BoW..."
python ${SCRIPT_PATH}/get_bag_of_word.py $FILE_LIST_PATH $ASR_PATH $BOW_PATH

# use Weka to train the model and classify the test data
for eventNum in 1 2 3
do
    echo "  Train and test Event ${eventNum}"
    # use logistic regression with default parameters
    java -cp ${WEKA_PATH}/weka.jar weka.classifiers.functions.Logistic -R 1.0E-8 -M -1 -t ${BOW_PATH}/train_${eventNum}.csv -T ${BOW_PATH}/test_${eventNum}.csv > ${RESULT_PATH}/asr_${eventNum}.out
done