import argparse
from src.utilities import get_dataset_df
from src.svm.svm import vectorize_tfidf, vectorize_fasttext
from sklearn import svm
import numpy as np
import pandas as pd


def train(train_vectors, train_labels):
    classifier_liblinear = svm.LinearSVC(C=0.5)
    classifier_liblinear.fit(train_vectors, train_labels)
    return classifier_liblinear


def predict(classifier: svm.SVC, vectors):
    prediction = classifier.predict(vectors)
    return prediction


def predict_centroid_class(classifier: svm.SVC, vectors):
    centroid = np.mean(vectors, axis=0).reshape(1, -1)
    predicted_class = classifier.predict(centroid)[0]
    return predicted_class


def main():
    parser = argparse.ArgumentParser(description='Logistic regression model for tweet author profiling')
    parser.add_argument('--c0_train', default="../../data/tok/nonhaters_en.tok.txt")
    parser.add_argument('--c1_train', default="../../data/tok/haters_en.tok.txt")
    parser.add_argument('--c0_test', default="../../data/tok/test/nonhaters_en.tok.txt")
    parser.add_argument('--c1_test', default="../../data//tok/test/haters_en.tok.txt")
    parser.add_argument('--fasttext', default=False)
    parser.add_argument('--lang', default='en')
    parser.add_argument('--out', default='Nahuel-Martin_svm_en.txt')
    args = parser.parse_args()


    # Load training datafame and evaluation dataframe
    train_df = get_dataset_df(args.c0_train, args.c1_train, with_authors=False)
    test_df = get_dataset_df(args.c0_test, args.c1_test, with_authors=True)

    # Vectorize datasets
    if args.fasttext:
        train_vectors, test_vectors, _ = vectorize_fasttext(train_df, test_df, train_df, lang=args.lang)
    else:
        train_vectors, test_vectors, _ = vectorize_tfidf(train_df, test_df, train_df)


    # Train
    classifier_liblinear = train(train_vectors, train_df['labels'])

    # Predict tweets
    test_df['labels'] = predict(classifier_liblinear, test_vectors)
    # Predict authors
    predicted_authors = [predict_centroid_class(classifier_liblinear, test_vectors[i * 200:(i * 200) + 200]) for
                         i, label in enumerate(test_df['labels'][::200])]
    predicted_authors_ids = [test_df['authors'][i] for i in range(0, test_df.shape[0], 200)]

    with open(args.out, 'w') as f:
        for author, label in zip(predicted_authors_ids, predicted_authors):
            f.write(f'{author}\t{args.lang}\t{label}\n')


if __name__ == '__main__':
    main()