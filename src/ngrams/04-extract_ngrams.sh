#!/bin/bash

[ "$#" -ne 4 ] && echo "04-extract_ngrams.sh <in-tok-file> <out-lm-file> <order>" && exit 1

IN_FILE=$1
OUT_FILE=$2
ORDER=$3

lmplz -o ${ORDER} < ${IN_FILE} > ${OUT_FILE}
build_binary ${OUT_FILE} ${OUT_FILE}.bin
# We only want .arpa.bin LMs, remove .arpa
rm ${OUT_FILE}