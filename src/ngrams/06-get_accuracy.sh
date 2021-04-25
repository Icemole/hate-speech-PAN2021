#!/bin/bash

[ "$#" -ne 1 ] && echo "06-get_accuracy_wrapper.sh <reco-dir>" && exit 1

RECO_DIR=$1
ORDER="2 3 4 5 6"
# ORDER=5

DIR_NAME=$(dirname $0)

for lang in en es
do
	echo ""
	echo "######"
	echo "  "${lang}
	echo "######"
	for order in $ORDER
	do
		echo "Order ${order}"
		awk -v ishater=${ishater} -v order=${order} '{if ((ishater == "" && $1 == 1) || (ishater == "non" && $1 == 0)) correct += 1} END {printf "Acc %shaters: %.2f%\n",  ishater, 100 * correct / NR}' ${RECO_DIR}/${ishater}haters_${lang}_reco.order-${order}.txt
	done
done
