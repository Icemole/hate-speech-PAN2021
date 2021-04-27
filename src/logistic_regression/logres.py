import argparse
from src.utilities import get_dataset_df
from sklearn.linear_model import LogisticRegressionCV


def main():
    parser = argparse.ArgumentParser(description='SVM model for tweet author profiling')
    parser.add_argument('--c0_train', default="../../data/tok/nonhaters_en.tok.train.txt")
    parser.add_argument('--c1_train', default="../../data/tok/haters_en.tok.train.txt")
    parser.add_argument('--c0_eval', default="../../data/tok/nonhaters_en.tok.eval.txt")
    parser.add_argument('--c1_eval', default="../../data/tok/haters_en.tok.eval.txt")
    parser.add_argument('--vectorization', choices=["count", "fasttext"], default="count")
    parser.add_argument('--lang', choices=["en", "es"], default="en")
    args = parser.parse_args()


    # Load training datafame and evaluation dataframe
    train_df = get_dataset_df(args.c0_train, args.c1_train)
    train_df = train_df.sample(frac=1)
    eval_df = get_dataset_df(args.c0_eval, args.c1_eval)


if __name__ == '__main__':
    main()