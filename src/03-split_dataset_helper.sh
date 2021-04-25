#!/bin/bash

([ "$#" -ne 4 ] && [ "$#" -ne 5 ]) && echo "03-split_dataset_helper.sh <dataset-dir> <eval-prop> <dev-prop> <out-dir> [--grouped]" && exit 1

IN_DIR=$1
EVAL_PROP=$2
DEV_PROP=$3
OUT_DIR=$4
SCRIPT_DIR=$(dirname $0)

rm ${OUT_DIR}/* 2> /dev/null
mkdir -p ${OUT_DIR}

for f in ${IN_DIR}/*.txt
do
    python ${SCRIPT_DIR}/03-split_dataset.py --dataset ${f} --eval_proportion ${EVAL_PROP} --dev_proportion ${DEV_PROP} --extract_to ${OUT_DIR}
    [ "$#" -eq 5 ] && python ${SCRIPT_DIR}/03-split_dataset.py --dataset ${f} --eval_proportion ${EVAL_PROP} --dev_proportion ${DEV_PROP} --extract_to ${OUT_DIR} --grouped
done