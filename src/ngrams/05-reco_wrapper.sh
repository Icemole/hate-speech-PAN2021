#!/bin/bash

[ "$#" -ne 3 ] && echo "05-reco_wrapper.sh <in-dir> <out-dir> <lm-dir>" && exit 1

DIRNAME=$(dirname $0)
# IN_DIR=../../data/tok
IN_DIR=$1
# OUT_DIR=../../results/ngrams
OUT_DIR=$2
# LM_DIR=../../models/ngrams/bin-lms
LM_DIR=$3

for lang in en es
do
    for order in 3 4
    do
        for ishater in "" non
        do
            ${DIRNAME}/05-reco.sh ${IN_DIR}/${ishater}haters_${lang}.tok.eval.txt ${OUT_DIR}/${ishater}haters_${lang}_reco.order-${order}.txt ${LM_DIR}/nonhaters_${lang}.order-${order}.arpa.bin ${LM_DIR}/haters_${lang}.order-${order}.arpa.bin
        done
    done
done