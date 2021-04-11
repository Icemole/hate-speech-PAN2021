import argparse
import fasttext


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', default='pan2021.train.en')
    parser.add_argument('--eval', default='pan2021.eval.en')
    parser.add_argument('--model_name', default='model.bin')
    args = parser.parse_args()

    # use loss="hs" (hierarchical softmax) for big datasets to approximate the softmax, speeding up training at the cost of some precision
    model = fasttext.train_supervised(input=args.train, lr=1.0, epoch=25, wordNgrams=2, dim=50)
    model.test(args.eval)
    model.save_model(args.model_name)


if __name__ == '__main__':
    main()
