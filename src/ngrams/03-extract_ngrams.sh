#!/bin/bash

rm -r ../../models/ngrams
mkdir -p ../../models/ngrams/bin-lms

for lang in en es
do
	for order in 3 4
	do
		for ishater in "" non
		do
			lmplz -o ${order} < ../../data/tok/${ishater}haters_${lang}.tok.train.txt > ../../models/ngrams/${ishater}haters_${lang}.order-${order}.arpa
			build_binary ../../models/ngrams/${ishater}haters_${lang}.order-${order}.arpa ../../models/ngrams/bin-lms/${ishater}haters_${lang}.order-${order}.arpa.bin
			# rm ../../models/${ishater}haters_${lang}.order-${order}.arpa
		done
	done
done
