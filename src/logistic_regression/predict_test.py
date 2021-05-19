import argparse
from src.utilities import get_dataset_df, get_test_dataset_df
from src.svm.svm import vectorize_tfidf, vectorize_fasttext
from sklearn.linear_model import LogisticRegression


def train(vectors, labels):
    lr = LogisticRegression(penalty='l2', C=0.5, solver='liblinear')
    clf = lr.fit(vectors, labels)
    return clf


def main():
    parser = argparse.ArgumentParser(description='Logistic regression model for tweet author profiling')
    parser.add_argument('--c0_train', default="../../data/tok/nonhaters_en.tok.txt")
    parser.add_argument('--c1_train', default="../../data/tok/haters_en.tok.txt")
    parser.add_argument('--test', default="../../data/tok/test/en.tok.txt")
    parser.add_argument('--fasttext', default=False)
    parser.add_argument('--lang', default='en')
    parser.add_argument('--out', default='Nahuel-Martin_svm_en2.txt')
    args = parser.parse_args()


    # Load training datafame and evaluation dataframe
    train_df = get_dataset_df(args.c0_train, args.c1_train, with_authors=False)
    test_df = get_test_dataset_df(args.test)

    # Vectorize datasets
    if args.fasttext:
        train_vectors, test_vectors, _ = vectorize_fasttext(train_df, test_df, train_df, lang=args.lang)
    else:
        train_vectors, test_vectors, _ = vectorize_tfidf(train_df, test_df, train_df)

    # Train model
    clf = train(train_vectors, train_df['labels'])

    # Predict
    prediction = clf.predict(test_vectors)
    test_df['labels'] = prediction

    authors = []
    labels = []
    for i in range(0, test_df.shape[0], 200):
        labels_auth_c1 = sum(1 for label in test_df['labels'][i:i + 200] if label == 1)
        authors.append(test_df['authors'][i])
        if labels_auth_c1 > 100:
            labels.append(1)
        else:
            labels.append(0)

    with open(args.out, 'w') as f:
        for author, label in zip(authors, labels):
            f.write(f'{author}\t{args.lang}\t{label}\n')


if __name__ == '__main__':
    main()