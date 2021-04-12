import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--c0_train', default='../../data/nonhaters_en.tok.train.txt')
    parser.add_argument('--c1_train', default='../../data/haters_en.tok.train.txt')
    parser.add_argument('--c0_eval', default='../../data/nonhaters_en.tok.eval.txt')
    parser.add_argument('--c1_eval', default='../../data/haters_en.tok.eval.txt')
    parser.add_argument('--out_train', default='pan2021.train.en')
    parser.add_argument('--out_eval', default='pan2021.eval.en')
    args = parser.parse_args()

    # Preproc data to match format as seen here https://fasttext.cc/docs/en/supervised-tutorial.html
    with open(args.out_train, 'w') as outrain:
        with open(args.c0_train, 'r') as f:
            for line in f.readlines():
                # taking 'nonhater' as 0 and 'hater' as 1
                outrain.write(f"__label__nonhater {line}")
        with open(args.c1_train, 'r') as f:
            for line in f.readlines():
                # taking 'nonhater' as 0 and 'hater' as 1
                outrain.write(f"__label__hater {line}")

    with open(args.out_eval, 'w') as outeval:
        with open(args.c0_eval, 'r') as f:
            for line in f.readlines():
                # taking 'nonhater' as 0 and 'hater' as 1
                outeval.write(f"__label__nonhater {line}")
        with open(args.c1_eval, 'r') as f:
            for line in f.readlines():
                # taking 'nonhater' as 0 and 'hater' as 1
                outeval.write(f"__label__hater {line}")


if __name__ == '__main__':
    main()
