#!/bin/bash

[ "$#" -ne 4 ] && echo "03-split_dataset_grouped.sh <dataset> <proportion-dev> <proportion-eval> <dir-out>" && exit 1

mkdir -p $4

FILE=$1
FILENAME=$(basename $1 | cut -d "." -f 1)
OUT_DIR=$4
LINES_TOTAL=$(wc -l $1 | cut -d " " -f 1)
calc() { awk "BEGIN{print $*}"; }
LINES_DEV=$(calc ${LINES_TOTAL}*$2)
LINES_EVAL=$(calc ${LINES_TOTAL}*$3)
LINES_TRAIN=$(calc ${LINES_TOTAL}-${LINES_DEV}-${LINES_EVAL})
shuf $1 > ${OUT_DIR}/aux.txt
head -n ${LINES_DEV} ${FILE} > ${OUT_DIR}/${FILENAME}.dev.tok.txt
tail -n +${LINES_DEV} ${FILE} | head -n ${LINES_EVAL} > ${OUT_DIR}/${FILENAME}.eval.tok.txt
tail -n +$(calc ${LINES_DEV}+${LINES_EVAL}) ${FILE} | head -n ${LINES_TRAIN} > ${OUT_DIR}/${FILENAME}.train.tok.txt
rm ${OUT_DIR}/aux.txt
