import numpy as np
import scipy.stats
from sklearn.model_selection import train_test_split


norms = {}
timestamps = {}

MEAN = None
STD = None
MIN = 20000
MAX = 0
normal  = scipy.stats.norm(4.5, 1.08)
features, labels = ([],[])

from sklearn.base import BaseEstimator, ClassifierMixin
class Attack(BaseEstimator, ClassifierMixin):

    def __init__ (self):
        self.mean = MEAN
        self.std = STD
        self.time_period = features[:,1]
        self.labels = labels
        self.normal = scipy.stats.norm(self.mean, self.std)

    def fit(self, X, y):
        return None

    def get_params(self,deep=True):
        return {}

    def predict(self, time_data):
        valid_points = get_valid_points(time_data, self.time_period, MIN, MAX)
        if  len(valid_points[0]) == 0:
            return np.random.choice(np.arange(self.time_period.shape[0]),1)
        else:
            pdfs = np.vectorize(self.normal.pdf)
            points = self.time_period[valid_points[0]] - time_data
            index = np.argmax(pdfs(points))
            return valid_points[0][index]
    
    def score(self, test_feat, test_labels):
        predictions = np.zeros(test_feat.shape[0])
        for i in range(test_feat.shape[0]):
            index = self.predict(test_feat[i,0])

            predictions[i] = self.labels[index]
        return np.mean(np.where(test_labels == predictions, 1, 0))



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
        pdfs = np.vectorize(normal.pdf)
        points = time_period[valid_points[0]] - time_data
        index = np.argmax(pdfs(points))
        return valid_points[0][index]


def score(estimator, test_feat, test_labels):
    predictions = np.zeros(test_feat.shape[0])
    for i in range(test_feat.shape[0]):
        index = estimator.predict(test_feat[i,0])
        predictions[i] = estimator.labels[index]
    return np.mean(np.where(test_labels == predictions, 1, 0))


features, labels = get_all_data('TrainingData/training-50-users.csv')
x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=.2, random_state=42)

means = np.zeros(np.unique(labels).shape[0])
std_devs = np.zeros(np.unique(labels).shape[0])
for label in np.unique(labels):
    if label != -1:
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

MEAN = 4.0
print(np.mean(means))
print(np.mean(std_devs))
STD = 1.3
normal  = scipy.stats.norm(MEAN, STD)
print(MEAN)
print(STD)
clf  = Attack()

real_labels = np.where(labels != -1)


from sklearn.model_selection import cross_val_score
a = cross_val_score(clf, features[real_labels], labels[real_labels], cv=5)
print(a.mean())
print(a.std())