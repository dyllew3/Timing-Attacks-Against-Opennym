import numpy as np
import scipy.stats
from sklearn.model_selection import train_test_split


norms = {}
timestamps = {}

MEAN = None
STD = None
MIN = 20000
MAX = 0
features, labels = ([],[])
GROUPS = [25, 50, 100]
NUM_GROUPS = 10

from sklearn.base import BaseEstimator, ClassifierMixin
class Attack(BaseEstimator, ClassifierMixin):

    def __init__ (self):
        self.mean = MEAN
        self.std = STD
        self.time_period = features[:,1]
        self.labels = labels
        self.normal = scipy.stats.norm(self.mean, self.std)
        self.num_groups = NUM_GROUPS

    def fit(self, X, y):
        return None

    def get_params(self,deep=True):
        return {}


    def predict(self, time_data):
        result = []
        for i in range(NUM_GROUPS):
            valid_points = get_valid_points(time_data, self.time_period, MIN*(i + 1), MAX* (i + 1))
            if  len(valid_points[0]) == 0:
                return np.random.choice(np.arange(self.time_period.shape[0]),1)
            else:
                normal = scipy.stats.norm(self.mean*(i + 1), self.std*(i + 1))
                pdfs = np.vectorize(normal.pdf)
                points = self.time_period[valid_points[0]] - time_data
                index = np.argmax(pdfs(points))
                result.append(valid_points[0][index])
        return np.array(result)
    
    def score(self, test_feat, test_labels):
        predictions = np.zeros((test_feat.shape[0], NUM_GROUPS))
        for i in range(test_feat.shape[0]):
            index = self.predict(test_feat[i,0])
            predictions[i] = self.labels[index]
        return np.mean(self.stripping_pred(predictions, test_labels))

    def stripping_pred(self, predicitions, labels):
        results = np.zeros(predicitions.shape[0])
        for i in range(predicitions.shape[0]):
            count = np.bincount(np.array(predicitions[i], dtype='int64'))
            if len(count) > int(labels[i]):
                results[i] = count[int(labels[i])]/ np.sum(count)
        return results



def get_all_data(filename,delimiter=','):
    all_data = np.genfromtxt(filename, delimiter=delimiter)
    # Randomly sample from the input file if it is for testing data
    features = all_data[:, :-1]
    labels = all_data[:, all_data.shape[1] - 1].ravel()
    return features, labels


def get_valid_points(time_stamp, time_period, min_val, max_val):
    abv_min = ((time_period - time_stamp) >= min_val)
    below_max = ((time_period - time_stamp) <= max_val)
    indexes = np.where(abv_min & below_max)
    if not indexes:
        return ()
    else:
        return indexes

def predict(time_data, time_period, normal):
    valid_points = get_valid_points(time_data, time_period, MIN, MAX)
    if  len(valid_points[0]) == 0:
        return np.random.choice(np.arange(time_period.shape[0]),1)
    else:
        points = time_period[valid_points[0]] - time_data
        index = np.argmax(normal.pdf(points))
        return valid_points[0][index]


def score(estimator, test_feat, test_labels):
    predictions = np.zeros(test_feat.shape[0], NUM_GROUPS)
    print("here")
    for i in range(test_feat.shape[0]):
        index = estimator.predict(test_feat[i,0])
        print(index)
        predictions[i,:] = estimator.labels[index]
    return np.mean(np.where(test_labels == predictions, 1, 0))

def latency_to_add(feats, length):
    a = np.zeros((length, 2))
    a[:, 0] = 1.2 * (np.random.randn(length) + 20)
    a[:, 1] = a[:, 0]
    return feats + a

features, labels = get_all_data('TrainingData/training-50-users(1).csv')
features = latency_to_add(features, features.shape[0])


means = np.zeros(np.unique(labels).shape[0])
std_devs = np.zeros(np.unique(labels).shape[0])

for label in np.unique(labels):
    timestamp_labels = features[np.where(labels == label)]
    timestamps[label] = timestamp_labels
    diffs = timestamp_labels[1:, 0] - timestamp_labels[: timestamp_labels.shape[0] - 1, 1]
    mu = np.mean(diffs)
    MAX = max(MAX, np.max(diffs))
    MIN = min(MIN, np.min(diffs))
    sigma = np.std(diffs)
    #print('for {} mean is {} std is {}, max is {}, min is {}'.format(label, mu, sigma, max_val, min_val))
    means[int(label)] = mu
    std_devs[int(label)] = sigma

MEAN = 4.8
STD = 1.22
normal  = scipy.stats.norm(MEAN, STD)
print("Set mean is {}".format(MEAN))
print("Set std is {}".format(STD))

from sklearn.model_selection import cross_val_score

for group in GROUPS:
    NUM_GROUPS = group
    print("Group size {}".format(NUM_GROUPS))
    clf  = Attack()
    a = cross_val_score(clf, features, labels, cv=5)
    print("{}, {}".format(a.mean(), a.std()))