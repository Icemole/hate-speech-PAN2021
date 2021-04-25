#!/bin/bash

[ "$#" -ne 2 ] && echo "04-extract_ngrams_helper.sh <in-tok-dir> <out-lm-dir> [--grouped]" && exit 1

# IN_DIR=../../data/tok
IN_DIR=$1
# OUT_DIR=../../models/ngrams/bin-lms
OUT_DIR=$2
ORDER="2 3 4 5 6"

rm -r ${OUT_DIR} 2> /dev/null
mkdir -p ${OUT_DIR}

DIR_NAME=$(dirname $0)

for lang in en es
do
	for order in ${ORDER}
	do
		for ishater in "" non
		do
			${DIR_NAME}/04-extract_ngrams.sh ${IN_DIR}/${ishater}haters_${lang}.tok.train.txt ${OUT_DIR}/${ishater}haters_${lang}.order-${order}.arpa ${order}
		done
	done
done
