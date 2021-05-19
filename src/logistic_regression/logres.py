import argparse
import pandas as pd
from src.utilities import get_dataset_df, author_estimation_boxplot
from src.svm.svm import vectorize_tfidf, vectorize_fasttext
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


def train(vectors, labels):
    lr = LogisticRegression(penalty='l2', C=0.5, solver='liblinear')
    clf = lr.fit(vectors, labels)
    return clf


def main():
    parser = argparse.ArgumentParser(description='Logistic regression model for tweet author profiling')
    parser.add_argument('--c0_train', default="../../data/tok/partitioned_data/nonhaters_es.tok.train.txt")
    parser.add_argument('--c1_train', default="../../data/tok/partitioned_data/haters_es.tok.train.txt")
    parser.add_argument('--c0_eval', default="../../data/tok/partitioned_data/nonhaters_es.tok.eval.txt")
    parser.add_argument('--c1_eval', default="../../data/tok/partitioned_data/haters_es.tok.eval.txt")
    parser.add_argument('--c0_dev', default="../../data/tok/partitioned_data/nonhaters_es.tok.dev.txt")
    parser.add_argument('--c1_dev', default="../../data/tok/partitioned_data/haters_es.tok.dev.txt")
    parser.add_argument('--fasttext', default=False)
    parser.add_argument('--lang', default='es')
    args = parser.parse_args()


    # Load training datafame and evaluation dataframe
    train_df = get_dataset_df(args.c0_train, args.c1_train)
    train_df = train_df.sample(frac=1)
    eval_df = get_dataset_df(args.c0_eval, args.c1_eval)
    dev_df = get_dataset_df(args.c0_dev, args.c1_dev)

    # Vectorize datasets
    if args.fasttext:
        train_vectors, eval_vectors, dev_vectors = vectorize_fasttext(train_df, eval_df, dev_df, lang=args.lang)
    else:
        train_vectors, eval_vectors, dev_vectors = vectorize_tfidf(train_df, eval_df, dev_df)

    # Train model
    clf = train(train_vectors, train_df['labels'])

    # Evaluate model for tuning
    mean_acc = clf.score(dev_vectors, dev_df["labels"])
    prediction = clf.predict(dev_vectors)
    print(classification_report(dev_df["labels"], prediction))

    print("\n###### Author tweet labeling distribution as boxplots - DEV ######")
    author_estimation_boxplot(ground_truth_df=dev_df,
                              predictions_df=pd.DataFrame({"text": dev_df["text"], "labels": prediction}))

    # Final result
    prediction = clf.predict(eval_vectors)
    print(classification_report(eval_df["labels"], prediction))

    print("\n###### Author tweet labeling distribution as boxplots - EVAL ######")
    author_estimation_boxplot(ground_truth_df=eval_df,
                              predictions_df=pd.DataFrame({"text": eval_df["text"], "labels": prediction}))


if __name__ == '__main__':
    main()