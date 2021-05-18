import pandas as pd
import matplotlib.pyplot as plt


def load_prediction_file(path):
    with open(path, 'r') as f:
        text = []
        labels = []
        for line in f.readlines():
            t, l = line.split('\t')
            text.append(t)
            labels.append(l)
        df = pd.DataFrame({'text': text, 'labels': labels})
        return df


def get_test_dataset_df(dataset):
    text = []
    authors = []
    with open(dataset, 'r') as f:
        for line in f.readlines():
            text.append(line.split('\t')[1].replace('\n', ''))
            authors.append(line.split('\t')[0])
    df = pd.DataFrame({'text': text, 'authors': authors})
    return df


def get_dataset_df(c0_dataset, c1_dataset, with_authors=False):
    # Build training dataframe
    labels = []
    text = []
    if with_authors:
        authors = []
        with open(c0_dataset, 'r') as f:
            for line in f.readlines():
                # Taking 'nonhater' as 0 and 'hater' as 1
                labels.append(0)
                text.append(line.split('\t')[1].replace('\n', ''))
                authors.append(line.split('\t')[0])
        with open(c1_dataset, 'r') as f:
            for line in f.readlines():
                # Taking 'nonhater' as 0 and 'hater' as 1
                labels.append(1)
                text.append(line.split('\t')[1].replace('\n', ''))
                authors.append(line.split('\t')[0])
        df = pd.DataFrame({'labels': labels, 'text': text, 'authors': authors})
    else:
        with open(c0_dataset, 'r') as f:
            for line in f.readlines():
                # Taking 'nonhater' as 0 and 'hater' as 1
                labels.append(0)
                text.append(line.replace('\n', ''))
        with open(c1_dataset, 'r') as f:
            for line in f.readlines():
                # Taking 'nonhater' as 0 and 'hater' as 1
                labels.append(1)
                text.append(line.replace('\n', ''))
        df = pd.DataFrame({'labels': labels, 'text': text})
    return df


def author_estimation_boxplot(predictions_df, ground_truth_df):
    aligned_df = predictions_df.merge(ground_truth_df, on=['text'], suffixes=('_predicted', '_ground_truth'),
                                      how='outer')
    c0_labels_auth_c0 = []
    c1_labels_auth_c1 = []
    for i in range(0, aligned_df.shape[0], 200):
        if aligned_df['labels_ground_truth'][i] == 0:
            c0_labels_auth_c0.append(sum(1 for label in aligned_df['labels_predicted'][i:i+200] if label == 0))
        else:
            c1_labels_auth_c1.append(sum(1 for label in aligned_df['labels_predicted'][i:i+200] if label == 1))

    auth_estimation_df_nonhater = pd.Series(c0_labels_auth_c0, name='nonhater_tweets_predicted_for_nonhater_auth')
    auth_estimation_df_hater = pd.Series(c1_labels_auth_c1, name='hater_tweets_predicted_for_hater_auth')
    df = pd.concat([auth_estimation_df_nonhater, auth_estimation_df_hater], axis=1)
    axes = df.boxplot(column=['nonhater_tweets_predicted_for_nonhater_auth', 'hater_tweets_predicted_for_hater_auth'],
                      vert=False, return_type='axes')
    plt.show()


if __name__ == '__main__':
    pass