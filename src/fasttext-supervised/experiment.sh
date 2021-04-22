DIMS="64 128 256"
ORDER="1 2" # 3 4 5 6"
LR="10.0 1.0"


for order in ${ORDER}
do
    for dim in ${DIMS}
    do
        for lr in ${LR}
        do
            python train.py --train pan2021_grouped.train.en --eval pan2021_grouped.eval.en --dim ${dim} --ngram_order ${order} --lr ${lr} --model_name model_${order}gram_${dims}dims_lr_${lr}.bin --write_accuracies accs_grouped.txt
        done
    done
done
#python train.py --dim 300 --epochs 200 --ngram_order 4 --lr 1.0 --model_name 200epochs_model_${order}gram_${dims}dims_lr_${lr}.bin
