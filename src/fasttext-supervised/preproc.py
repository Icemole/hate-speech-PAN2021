import argparse


def main():
    parser = argparse.ArgumentParser(description='Translator of news from Spanish to English')
    parser.add_argument('--c0_train', default='../../data/nonhaters_en.txt')
    parser.add_argument('--c1_train', default='../../data/haters_en.txt')
    parser.add_argument('--c0_eval', default='../../data/nonhaters_en.txt')
    parser.add_argument('--c1_eval', default='../../data/haters_en.txt')
    args = parser.parse_args()

    # TODO preproc data to match format as seen here https://fasttext.cc/docs/en/supervised-tutorial.html


if __name__ == '__main__':
    main()