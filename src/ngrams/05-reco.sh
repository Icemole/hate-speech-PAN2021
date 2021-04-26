#!/bin/bash

[ "$#" -ne 4 ] && echo "05-reco.sh <in-file> <out-file> <nonhaters-lm-file> <haters-lm-file>" && exit 1
IN_FILE=$1
OUT_FILE=$2
NONHATERS_LM_FILE=$3
HATERS_LM_FILE=$4

query ${NONHATERS_LM_FILE} < ${IN_FILE} > tmp_reco_by_nonhaters.probs
query ${HATERS_LM_FILE} < ${IN_FILE} > tmp_reco_by_haters.probs

cat tmp_reco_by_nonhaters.probs | head -n -4 | awk '{print $(NF-2)}' > tmp_reco_by_nonhaters.phrase-probs
cat tmp_reco_by_haters.probs | head -n -4 | awk '{print $(NF-2)}' > tmp_reco_by_haters.phrase-probs

paste tmp_reco_by_nonhaters.phrase-probs tmp_reco_by_haters.phrase-probs | awk '{if($1 > $2) {print 0;} else {print 1;}}' > tmp_labels.txt
paste tmp_labels.txt ${IN_FILE} > ${OUT_FILE}
rm *.probs *.phrase-probs tmp_labels.txt