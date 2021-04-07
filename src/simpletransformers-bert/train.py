import argparse
import json
import pandas as pd
from simpletransformers.classification import ClassificationModel


def main():

    # Build training dataframe
    labels = []
    text = []
    with open('../../data/nonhaters_en.txt', 'r') as f:
        for line in f.readlines():
            # taking 'nonhater' as 0 and 'hater' as 1
            labels.append(0)
            text.append(line)
    with open('../../data/haters_en.txt', 'r') as f:
        for line in f.readlines():
            # taking 'nonhater' as 0 and 'hater' as 1
            labels.append(1)
            text.append(line)

    train_df = pd.DataFrame({'labels': labels, 'text': text})
    # Shuffle training samples
    train_df = train_df.sample(frac=1)

    # Instantiate BERT  model and train over training df
    model_args_file = open('model_args.json', 'r')
    model_args = json.load(model_args_file)
    model = ClassificationModel('roberta', 'roberta-base', args=model_args, use_cuda=False)
    model.train_model(train_df)

    # Evaluate model on evaluation df
    result, model_outputs, wrong_predictions = model.eval_model(eval_df)


if __name__ == '__main__':
    main()