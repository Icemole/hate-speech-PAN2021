import argparse
import fasttext


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', default='pan2021.train.en')
    parser.add_argument('--eval', default='pan2021.eval.en')
    parser.add_argument('--model_name', default=None)
    parser.add_argument('--epochs', default=25)
    parser.add_argument('--ngram_order', default=4)
    parser.add_argument('--dim', default=50)
    parser.add_argument('--lr', default=1.0)
    parser.add_argument('--write_accuracies', default=None)
    args = parser.parse_args()

    # use loss="hs" (hierarchical softmax) for big datasets to approximate the softmax, speeding up training at the cost of some precision
    model = fasttext.train_supervised(input=args.train, lr=float(args.lr), epoch=int(args.epochs), wordNgrams=int(args.ngram_order), dim=int(args.dim))
    if args.write_accuracies is None:
        print("Order = " + str(args.ngram_order) + " | Dim = " + str(args.dim) + " | LR = " + str(args.lr) + " | # Epochs = " + str(args.epochs))
        print(model.test(args.eval))
    else:
        with open(args.write_accuracies, "a") as f:
            f.write("Order = " + str(args.ngram_order) + " | Dim = " + str(args.dim) + " | LR = " + str(args.lr) + " | # Epochs = " + str(args.epochs))
            f.write("\n")
            f.write(str(model.test(args.eval)))
            f.write("\n")
            f.write("\n")
    if args.model_name is not None:
        model.save_model(args.model_name)


if __name__ == '__main__':
    main()
