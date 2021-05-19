import argparse
import json
import pandas as pd
from simpletransformers.classification import ClassificationModel
from src.utilities import author_estimation_boxplot
from sklearn.metrics import classification_report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--c0_train', default='../../data/tok/partitioned_data/nonhaters_es.tok.train.txt')
    parser.add_argument('--c1_train', default='../../data/tok/partitioned_data/haters_es.tok.train.txt')
    parser.add_argument('--c0_eval', default='../../data/tok/partitioned_data/nonhaters_es.tok.eval.txt')
    parser.add_argument('--c1_eval', default='../../data/tok/partitioned_data/haters_es.tok.eval.txt')
    parser.add_argument('--model_args', default='bert-multilingual-cased.json')
    args = parser.parse_args()

    # Build training dataframe
    labels = []
    text = []
    with open(args.c0_train, 'r') as f:
        for line in f.readlines():
            # taking 'nonhater' as 0 and 'hater' as 1
            labels.append(0)
            text.append(line)
    with open(args.c1_train, 'r') as f:
        for line in f.readlines():
            # taking 'nonhater' as 0 and 'hater' as 1
            labels.append(1)
            text.append(line)

    train_df = pd.DataFrame({'labels': labels, 'text': text})
    # Shuffle training samples
    train_df = train_df.sample(frac=1)

    # Build evaluation dataframe
    labels = []
    text = []
    with open(args.c0_eval, 'r') as f:
        for line in f.readlines():
            # taking 'nonhater' as 0 and 'hater' as 1
            labels.append(0)
            text.append(line)
    with open(args.c1_eval, 'r') as f:
        for line in f.readlines():
            # taking 'nonhater' as 0 and 'hater' as 1
            labels.append(1)
            text.append(line)

    eval_df = pd.DataFrame({'labels': labels, 'text': text})
    # Shuffle evaluation samples
    eval_df = eval_df.sample(frac=1)

    # Instantiate model and train over training df
    model_args_file = open(args.model_args, 'r')
    model_args = json.load(model_args_file)
    model = ClassificationModel(model_type=model_args['model_type'], model_name=model_args['model_name'],
                                args=model_args, use_cuda=False)
    model.train_model(train_df)

    # Evaluate model on evaluation df
    result, model_outputs, wrong_predictions = model.eval_model(eval_df)
    print(result)
    # Predict vectors
    prediction = model.predict(eval_df['text'])[0]

    print(classification_report(eval_df["labels"], prediction))

    print("\n###### Author tweet labeling distribution as boxplots - EVAL ######")
    author_estimation_boxplot(ground_truth_df=eval_df,
                              predictions_df=pd.DataFrame({"text": eval_df["text"], "labels": prediction}))


if __name__ == '__main__':
    main()
