#!/bin/bash

[ "$#" -ne 2 ] && echo "02-clean_helper.sh <plain-text-dir> <out-dir>" && exit 1

IN_DIR=$1
OUT_DIR=$2
SCRIPT_DIR=$(dirname $0)

rm ${OUT_DIR}/* 2> /dev/null
mkdir -p ${OUT_DIR}

for f in ${IN_DIR}/*
do
    FILENAME=$(basename ${f} | cut -d "." -f 1).tok.txt
    python ${SCRIPT_DIR}/02-clean.py --dataset ${f} --write_to ${OUT_DIR}/${FILENAME}
    echo "Finished processing ${FILENAME}"
done