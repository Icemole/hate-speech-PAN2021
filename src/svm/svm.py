import argparse
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import fasttext
from sklearn import svm
from sklearn.metrics import classification_report
from src.utilities import get_dataset_df, author_estimation_boxplot
import pandas as pd
import numpy as np


def vectorize_count(train_df, eval_df, dev_df):
    vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1,5))
    train_vectors = vectorizer.fit_transform(train_df['text'])
    eval_vectors = vectorizer.transform(eval_df['text'])
    dev_vectors = vectorizer.transform(dev_df['text'])
    return train_vectors, eval_vectors, dev_vectors


def vectorize_fasttext(train_df, eval_df, dev_df, lang, c0_train, c1_train):
    # TODO use different pretrained vectors depending on the language
    if lang == "es":
        pretrained = fasttext.train_unsupervised(c1_train, model='skipgram',
                                                 lr=0.05, dim=300, ws=5, epoch=10,
                                                 pretrainedVectors="wiki-news-300d-1M.vec")
    else:
        pretrained = fasttext.train_unsupervised(c1_train, model='skipgram',
                                                 lr=0.05, dim=300, ws=5, epoch=10,
                                                 pretrainedVectors="wiki-news-300d-1M.vec")


    train_vectors = [pretrained.get_sentence_vector(text.replace('\n', '')) for text in list(train_df['text'])]
    eval_vectors = [pretrained.get_sentence_vector(text.replace('\n', '')) for text in list(eval_df['text'])]
    dev_vectors = [pretrained.get_sentence_vector(text.replace('\n', '')) for text in list(dev_df['text'])]

    return train_vectors, eval_vectors, dev_vectors


def train(train_vectors, train_labels):
    classifier_liblinear = svm.SVC(C=0.5, kernel='rbf', gamma='scale')
    classifier_liblinear.fit(train_vectors, train_labels)
    return classifier_liblinear


def predict(classifier: svm.SVC, vectors):
    prediction = classifier.predict(vectors)
    return prediction


def predict_centroid_class(classifier: svm.SVC, vectors):
    centroid = np.mean(vectors, axis=0)
    predicted_class = classifier.predict(centroid)[0]
    return predicted_class


def evaluate(gt_df, predicted_df, gt_authors, predicted_authors):
    print("\n###### Accuracy breakdown over individual tweets ######")
    print(classification_report(gt_df["labels"], predicted_df["labels"]))

    print("\n###### Author tweet labeling distribution as boxplots ######")
    author_estimation_boxplot(ground_truth_df=gt_df, predictions_df=predicted_df)

    print("\n###### Author prediction using svm centroid ######")
    print(classification_report(gt_authors, predicted_authors))


def main():
    parser = argparse.ArgumentParser(description='SVM model for tweet author profiling')
    parser.add_argument('--c0_train', default="../../data/tok/partitioned_data/nonhaters_en.tok.train.txt")
    parser.add_argument('--c1_train', default="../../data/tok/partitioned_data/haters_en.tok.train.txt")
    parser.add_argument('--c0_eval', default="../../data/tok/partitioned_data/nonhaters_en.tok.eval.txt")
    parser.add_argument('--c1_eval', default="../../data/tok/partitioned_data/haters_en.tok.eval.txt")
    parser.add_argument('--c0_dev', default="../../data/tok/partitioned_data/nonhaters_en.tok.dev.txt")
    parser.add_argument('--c1_dev', default="../../data/tok/partitioned_data/haters_en.tok.dev.txt")
    parser.add_argument('--vectorization', choices=["tfidf", "fasttext"], default="fasttext")
    parser.add_argument('--lang', choices=["en", "es"], default="en")
    args = parser.parse_args()


    # Load training datafame and evaluation dataframe
    train_df = get_dataset_df(args.c0_train, args.c1_train)
    train_df = train_df.sample(frac=1)
    eval_df = get_dataset_df(args.c0_eval, args.c1_eval)
    dev_df = get_dataset_df(args.c0_dev, args.c1_dev)

    # Vectorize
    if args.vectorization == "fasttext":
        train_vectors, eval_vectors, dev_vectors = vectorize_fasttext(train_df, eval_df, dev_df, lang=args.lang,
                                                         c0_train=args.c0_train, c1_train=args.c1_train)
    else:
        train_vectors, eval_vectors, dev_vectors = vectorize_count(train_df, eval_df, dev_df)

    # Train
    classifier_liblinear = train(train_vectors, train_df['labels'])

    # Predict tweets
    prediction = predict(classifier_liblinear, dev_vectors)
    # Predict authors
    gt_authors = [label for label in eval_df['labels'][::200]]
    predicted_authors = [predict_centroid_class(classifier_liblinear, eval_vectors[i:i+200]) for i, label in enumerate(eval_df['labels'][::200])]

    # Evaluate
    predicted_df = pd.DataFrame({'text': list(dev_df['text']), 'labels': prediction})
    evaluate(gt_df=dev_df, predicted_df=predicted_df, gt_authors=gt_authors, predicted_authors=predicted_authors)


if __name__ == '__main__':
    main()