#!/bin/bash

# This script assumes the following structure:
#
# unpacked-dataset
# |
# |-- en
# |   |
# |   |-- <author1-id>.xml
# |   |-- <author2-id>.xml
# |   |-- ...
# |   |-- truth.txt
# |-- es
# |   |
# |   |-- <author1-id>.xml
# |   |-- <author2-id>.xml
# |   |-- ...
# |   |-- truth.txt

[ "$#" -ne 2 ] && echo "process_all.sh <unpacked-dataset>"

source env/bin/activate

mkdir tmp
mkdir tmp/plain_text
mkdir tmp/tok

mkdir out

# Data extraction and cleaning
python src/01-extract_text.py --extract_from $1 --extract_to tmp/plain_text
python src/02-clean_wrapper.sh --dataset tmp/plain_text --write_to tmp/tok

# Training