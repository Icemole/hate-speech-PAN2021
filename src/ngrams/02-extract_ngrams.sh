#!/bin/bash

rm -r ../../models/ngrams
mkdir -p ../../models/ngrams/bin-lms

for lang in en es
do
	for order in 3 4
	do
		for ishater in "" non
		do
			lmplz -o ${order} < ../../data/${ishater}haters_${lang}.txt > ../../models/${ishater}haters_${lang}.order-${order}.arpa
			build_binary ../../models/${ishater}haters_${lang}.order-${order}.arpa ../../models/bin-lms/${ishater}haters_${lang}.order-${order}.arpa.bin
		done
	done
done
