#!/bin/bash

[ "$#" -ne 2 ] && echo "02-clean_wrapper.sh <plain-text-dir> <out-dir>" && exit 1

DIR=$(dirname $0)
OUT_DIR=$2
for f in $1/*
do
    FILENAME=$(basename ${f})
    python 02-clean.py --dataset ${f} --write_to ${OUT_DIR}/${FILENAME}
done