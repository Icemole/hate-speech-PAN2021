#!/bin/bash

ORDER="3 4"
# ORDER=5

rm -r ../../results/ngrams
mkdir -p ../../results/ngrams

for lang in en es
do
    for order in 3 4
    do
        for ishater in "" non
        do
            query ../../models/ngrams/bin-lms/haters_${lang}.order-${order}.arpa.bin < ../../data/tok/${ishater}haters_${lang}.tok.eval.txt > ../../results/ngrams/${ishater}haters_reco_by_haters_${lang}.order-${order}.probs
            query ../../models/ngrams/bin-lms/nonhaters_${lang}.order-${order}.arpa.bin < ../../data/tok/${ishater}haters_${lang}.tok.eval.txt > ../../results/ngrams/${ishater}haters_reco_by_nonhaters_${lang}.order-${order}.probs
        done
    done
done