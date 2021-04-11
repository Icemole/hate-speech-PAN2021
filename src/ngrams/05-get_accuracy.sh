#!/bin/bash

for lang in en es
do
	echo ""
	echo "######"
	echo "  "${lang}
	echo "######"
	for order in 3 4
	do
		echo "Order ${order}"
		for ishater in "" non
		do
			cat ../../results/ngrams/${ishater}haters_reco_by_haters_${lang}.order-${order}.probs | head -n -4 | awk '{print $(NF-2)}' > ../../results/ngrams/${ishater}haters_reco_by_haters_${lang}.order-${order}.phrase-prob
            cat ../../results/ngrams/${ishater}haters_reco_by_nonhaters_${lang}.order-${order}.probs | head -n -4 | awk '{print $(NF-2)}' > ../../results/ngrams/${ishater}haters_reco_by_nonhaters_${lang}.order-${order}.phrase-prob
            paste ../../results/ngrams/${ishater}haters_reco_by_haters_${lang}.order-${order}.phrase-prob ../../results/ngrams/${ishater}haters_reco_by_nonhaters_${lang}.order-${order}.phrase-prob | awk -v ishater=${ishater} -v order=${order} '{if ((ishater == "" && $1 > $2) || (ishater == "non" && $1 < $2)) correct += 1} END {printf "Acc %shaters: %.2f%\n",  ishater, 100 * correct / NR}'
		done
	done
done
