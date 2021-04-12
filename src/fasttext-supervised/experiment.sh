DIMS="64 128 256"
ORDER="2 3 4 5 6"
LR="1.0 0.1 0.01"


for dim in ${DIMS}
do
    for order in ${ORDER}
    do
        for lr in ${LR}
        do
            python train.py --dim ${dim} --ngram_order ${order} --lr ${lr} --model_name model_${order}gram_${dims}dims_lr_${lr}.bin --write_accuracies accs.txt
        done
    done
done
