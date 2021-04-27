import pandas as pd


def get_dataset_df(c0_dataset, c1_dataset):
    # Build training dataframe
    labels = []
    text = []
    with open(c0_dataset, 'r') as f:
        for line in f.readlines():
            # Taking 'nonhater' as 0 and 'hater' as 1
            labels.append(0)
            text.append(line)
    with open(c1_dataset, 'r') as f:
        for line in f.readlines():
            # Taking 'nonhater' as 0 and 'hater' as 1
            labels.append(1)
            text.append(line)
    df = pd.DataFrame({'labels': labels, 'text': text})
    return df


def author_estimation_boxplot(predictions_df, ground_truth_df):
    aligned_df = predictions_df.merge(ground_truth_df, on=['text'], suffixes=('_predicted', '_ground_truth'),
                                      how='outer')
    c0_labels_auth_c0 = []
    c1_labels_auth_c1 = []
    for i in range(0, aligned_df.shape[0], 200):
        if aligned_df['labels_ground_truth'] == 0:
            c0_labels_auth_c0.append(sum(1 for label in aligned_df['labels_predicted'][i:i+200] if label == 0))
        else:
            c1_labels_auth_c1.append(sum(1 for label in aligned_df['labels_predicted'][i:i+200] if label == 1))


    auth_estimation_df = pd.DataFrame({'nonhater_tweets_predicted_for_nonhater_auth': c0_labels_auth_c0,
                                       'hater_tweets_predicted_for_hater_auth': c1_labels_auth_c1})
    auth_estimation_df.boxplot(column=['nonhater_tweets_predicted_for_nonhater_auth',
                                       'hater_tweets_predicted_for_hater_auth'])


if __name__ == '__main__':
    pass