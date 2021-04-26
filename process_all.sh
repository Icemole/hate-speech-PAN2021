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
src/02-clean_helper.sh tmp/plain_text tmp/tok
#src/03-split_dataset_helper.sh data/tok 0.1 0.05 data/tok/partitioned_data --grouped

# Training
src/ngrams/04-extract_ngrams_helper.sh data/tok/partitioned_data/ models/ngrams/bin-lms/
src/ngrams/05-reco_helper.sh data/tok/partitioned_data/ results/ngrams/ models/ngrams/bin-lms/
src/ngrams/06-get_accuracy.sh results/ngrams/