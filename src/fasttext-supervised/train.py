import argparse
import fasttext


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', default='pan2021.train.en')
    parser.add_argument('--eval', default='pan2021.eval.en')
    parser.add_argument('--model_name', default='model.bin')
    args = parser.parse_args()

    model = fasttext.train_supervised(input=args.train)
    model.test(args.eval)
    model.save_model(args.model_name)


if __name__ == '__main__':
    main()
