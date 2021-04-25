#!/bin/bash

[ "$#" -ne 3 ] && echo "05-reco_helper.sh <in-dir> <out-dir> <lm-dir>" && exit 1

DIRNAME=$(dirname $0)
# IN_DIR=../../data/tok
IN_DIR=$1
# OUT_DIR=../../results/ngrams
OUT_DIR=$2
# LM_DIR=../../models/ngrams/bin-lms
LM_DIR=$3
ORDER="2 3 4 5 6"

rm ${OUT_DIR}/* 2> /dev/null
mkdir -p ${OUT_DIR}

for lang in en es
do
    for order in ${ORDER}
    do
        for ishater in "" non
        do
            # If .bin LMs exist, recognize with them; if not, recognize with .arpa
            ([ -f "${LM_DIR}/nonhaters_${lang}.order-${order}.arpa.bin" ] && [ -f "${LM_DIR}/haters_${lang}.order-${order}.arpa.bin" ] \
            && ${DIRNAME}/05-reco.sh ${IN_DIR}/${ishater}haters_${lang}.tok.eval.txt ${OUT_DIR}/${ishater}haters_${lang}_reco.order-${order}.txt ${LM_DIR}/nonhaters_${lang}.order-${order}.arpa.bin ${LM_DIR}/haters_${lang}.order-${order}.arpa.bin) \
            || ${DIRNAME}/05-reco.sh ${IN_DIR}/${ishater}haters_${lang}.tok.eval.txt ${OUT_DIR}/${ishater}haters_${lang}_reco.order-${order}.txt ${LM_DIR}/nonhaters_${lang}.order-${order}.arpa ${LM_DIR}/haters_${lang}.order-${order}.arpa
            
        done
    done
done