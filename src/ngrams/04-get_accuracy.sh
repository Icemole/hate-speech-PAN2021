#!/bin/bash

for lang in en es
do
	for order in 3 4
	do
		for ishater in "" non
		do
			cat ../../results/ngrams/${ishater}haters_reco_by_haters_${lang}.order-${order}.probs | head -n -4 | awk '{print $(NF-2)}' > ../../results/ngrams/${ishater}haters_reco_by_haters_${lang}.order-${order}.phrase-prob
            cat ../../results/ngrams/${ishater}haters_reco_by_nonhaters_${lang}.order-${order}.probs | head -n -4 | awk '{print $(NF-2)}' > ../../results/ngrams/${ishater}haters_reco_by_nonhaters_${lang}.order-${order}.phrase-prob
            paste ../../results/ngrams/${ishater}haters_reco_by_haters_${lang}.order-${order}.phrase-prob ../../results/ngrams/${ishater}haters_reco_by_nonhaters_${lang}.order-${order}.phrase-prob
            paste ../../results/ngrams/${ishater}haters_reco_by_haters_${lang}.order-${order}.phrase-prob ../../results/ngrams/${ishater}haters_reco_by_nonhaters_${lang}.order-${order}.phrase-prob | awk -v ishater=${ishater} -v order=${order} '{if ((ishater == "" && $1 > $2) || (ishater == "non" && $1 < $2)) correct += 1} END {printf "Acc %shaters order %d: %.2f%\n",  ishater, order, 100 * correct / NR}'
		done
	done
done
