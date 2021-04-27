#!/bin/bash

([ "$#" -ne 3 ] && [ "$#" -ne 4 ]) && echo "06-get_threshold.sh <dev-file> <nonhaters-lm-file> <haters-lm-file> [--grouped]" && exit 1

DEV_FILE=$1
NONHATERS_LM_FILE=$2
HATERS_LM_FILE=$3

DIR_NAME=$(dirname $0)
TMP_RECO_FILE=$(basename ${DEV_FILE} | cut -d "." -f 1).reco.txt
echo $TMP_RECO_FILE

rm -r threshold_by_author_${TMP_RECO_FILE} global_threshold_${TMP_RECO_FILE}

# Step 1: recognize the file
${DIR_NAME}/05-reco.sh ${DEV_FILE} ${TMP_RECO_FILE} ${NONHATERS_LM_FILE} ${HATERS_LM_FILE}

# Step 2: run this fancy script
NUM_LINES=$(wc -l ${DEV_FILE} | awk '{print $1}')
[ "$#" -ne 3 ] && BLOCK_SIZE=1 || BLOCK_SIZE=200
#NUM_BLOCKS=$(wc -l ${DEV_FILE} | awk -v GS=${BLOCK_SIZE} '{print $1/GS}')
func() {
    awk '{thr += $1} END {print thr}'
}
export -f func
split -l ${BLOCK_SIZE} ${TMP_RECO_FILE} #--filter "func() $FILE" > threshold_by_author_${TMP_RECO_FILE}
for f in x[[:alpha:]][[:alpha:]]
do
    awk '{thr += $1} END {print thr}' $f >> threshold_by_author_${TMP_RECO_FILE}
done
awk '{thr += $1} END {print thr/NR}' threshold_by_author_${TMP_RECO_FILE} > global_threshold_${TMP_RECO_FILE}

rm ${TMP_RECO_FILE} x[[:alpha:]][[:alpha:]]