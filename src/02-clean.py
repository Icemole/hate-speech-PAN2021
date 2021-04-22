import argparse
from nltk.tokenize import TweetTokenizer


def main():
    parser = argparse.ArgumentParser(description='Translator of news from Spanish to English')
    parser.add_argument('--dataset', default='data/plain_text/nonhaters_es.txt',
                        help='Path to plain-text data')
    parser.add_argument('--write_to', default=None,
                        help='Where to write the output of the cleaning process. If not declared, the extraction is done to the same directory where the dataset is located')
    args = parser.parse_args()

    # TweetTokenizer keeps hashtags intact while word_tokenize does not
    tokenizer = TweetTokenizer(preserve_case=True, reduce_len=False, strip_handles=False)

    if args.write_to is None:
        fout_name = f"{args.dataset.rsplit('.', 1)[0]}.tok.{args.dataset.rsplit('.', 1)[1]}"
    else:
        fout_name = args.write_to
    
    with open(args.dataset, 'r') as fin, open(fout_name, 'w') as fout:
        for line in fin.readlines():
            # Leave #USER#|#HASHTAG#|#URL# special token as #{SPECIAL_TOKEN} to avoid conflicts with the TweetTokenizer
            filtered_line = line.replace("#USER#", "#USER").replace("#HASHTAG#", "#HASHTAG").replace("#URL#", "#URL")
            tok_line = ' '.join(tokenizer.tokenize(filtered_line)) + '\n'
            fout.write(tok_line)


if __name__ == '__main__':
    main()
