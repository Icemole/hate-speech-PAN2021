import argparse
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import fasttext
from sklearn import svm
from sklearn.metrics import classification_report
from src.utilities import get_dataset_df


def vectorize_count(train_df, eval_df):
    vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1,3))
    train_vectors = vectorizer.fit_transform(train_df['text'])
    eval_vectors = vectorizer.transform(eval_df['text'])
    return train_vectors, eval_vectors


def vectorize_fasttext(train_df, eval_df, lang="en"):
    if lang == "es":
        pretrained = fasttext.train_unsupervised("../../data/tok/haters_es.tok.train.txt", model='skipgram',
                                                 lr=0.05, dim=300, ws=5, epoch=5)
    else:
        pretrained = fasttext.train_unsupervised("../../data/tok/haters_en.tok.train.txt", model='skipgram',
                                                 lr=0.05, dim=300, ws=5, epoch=5)


    train_vectors = [pretrained.get_sentence_vector(text.replace('\n', '')) for text in list(train_df['text'])]
    eval_vectors = [pretrained.get_sentence_vector(text.replace('\n', '')) for text in list(eval_df['text'])]

    return train_vectors, eval_vectors


def train(train_vectors, train_labels):
    classifier_liblinear = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
    classifier_liblinear.fit(train_vectors, train_labels)
    return classifier_liblinear


def predict(classifier: svm.SVC, dev_vectors, dev_labels):
    prediction = classifier.predict(dev_vectors)
    print(classification_report(dev_labels, prediction))
    return prediction


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
    # Vectorize
    if args.vectorization == "fasttext":
        train_vectors, eval_vectors = vectorize_fasttext(train_df, eval_df, lang=args.lang)
    else:
        train_vectors, eval_vectors = vectorize_count(train_df, eval_df)
    # Train
    classifier_liblinear = train(train_vectors, train_df['labels'])
    # Evaluate
    prediction = predict(classifier_liblinear, eval_vectors, eval_df['labels'])


if __name__ == '__main__':
    main()