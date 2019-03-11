import numpy as np
import scipy.stats



norms = {}
timestamps = {}


def get_all_data(filename,delimiter=','):
    all_data = np.genfromtxt(filename, delimiter=delimiter)
    # Randomly sample from the input file if it is for testing data
    features = all_data[:, :-1]
    labels = all_data[:, all_data.shape[1] - 1].ravel()
    return features, labels


def get_test(features, labels):
    test_amount = 0.
    amount = int(features.shape[0] * test_amount)
    return (features[:amount,:], labels[:amount], features[amount:, :], labels[amount:])

def get_valid_points(time_stamp, time_period, min_val, max_val):
    abv_min = ((time_period - time_stamp) >= min_val)
    below_max = ((time_period - time_stamp) <= max_val)
    return time_period[np.where(abv_min & below_max)]

def predict(time_data):
    label_probs = np.zeros(len(timestamps.keys()))
    for label in timestamps.keys():
        norm, max_val, min_val = norms[label]
        valid_points = get_valid_points(time_data[1], timestamps[label][:,1], min_val, max_val)
        diffs = valid_points - time_data[1]
        if len(list(diffs)) > 0:
            pdf = np.vectorize(norm.pdf)
            probs = pdf(diffs)
            label_probs[int(label)] = np.max(probs)
    return np.argmax(label_probs)

def score(test_feat, test_labels):
    predictions = np.zeros(test_feat.shape[0])
    for i in range(test_feat.shape[0]):
        predictions[i] = predict(test_feat[i,:])
    return np.mean(np.where(test_labels == predictions, 1, 0))


features, labels = get_all_data('TrainingData/ground_truth.csv')


for label in np.unique(labels):
    timestamp_labels = features[np.where(labels == label)]
    timestamps[label] = timestamp_labels
    diffs = timestamp_labels[1:, 0] - timestamp_labels[: timestamp_labels.shape[0] - 1, 1]
    mu = np.mean(diffs)
    max_val = np.max(diffs)
    min_val = np.min(diffs)
    sigma = np.std(diffs)
    #print('for {} mean is {} std is {}, max is {}, min is {}'.format(label, mu, sigma, max_val, min_val))
    norms[label] = (scipy.stats.norm(mu, sigma), max_val, min_val)


size=50
indexes = np.random.choice(range(features.shape[0]), size, replace=False)
features_test, labels_test = features[indexes], labels[indexes]


print(score(features_test, labels_test))