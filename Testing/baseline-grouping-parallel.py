import numpy as np
import scipy.stats
from sklearn.model_selection import train_test_split
import queue
import threading

norms = {}
timestamps = {}

NUM_THREADS = 10
LIKELY = queue.Queue()


MEAN = None
STD = None
MIN = 20000
MAX = 0
features, labels = ([],[])
GROUPS = [5, 10, 25, 50, 100]
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
        self.queue = queue.Queue()

    def fit(self, X, y):
        return None

    def get_params(self,deep=True):
        return {}

    def parallel_task(self, local_period, time_data):
        result = np.zeros((NUM_GROUPS, 2))
        for i in range(NUM_GROUPS):
            valid_points = get_valid_points(time_data, local_period, MIN*(i + 1), MAX* (i + 1))
            if  len(valid_points[0]) == 0:
                return np.random.choice(np.arange(self.time_period.shape[0]),1)
            else:
                normal = scipy.stats.norm(self.mean*(i + 1), self.std*(i + 1))
                pdfs = np.vectorize(normal.pdf)
                points = local_period[valid_points[0]] - time_data
                probs = pdfs(points)
                index = np.argmax(probs)
                result[i, 0] = (valid_points[0][index])
                result[i, 1] = probs[index]
        self.queue.put(result)


    def predict(self, time_data):
        step = self.time_period.shape[0] // NUM_THREADS
        threads = []
        for j in range(NUM_THREADS):
            local_period = self.time_period[j * step:] if j == NUM_THREADS - 1 else self.time_period[j * step:(j + 1) * step]
            thread = (threading.Thread(target=self.parallel_task, args=(local_period, time_data)))
            threads.append(thread)
            threads[j].start()
        for k in range(NUM_THREADS):
            threads[k].join()

        values = np.zeros((NUM_THREADS * NUM_GROUPS, 2))
        i = 0
        while not self.queue.empty():
            subset = self.queue.get()
            values[i: i + subset.shape[0], : ] = subset
            i += subset.shape[0]
        return values[values[:, 1].argsort()[::-1]][:NUM_GROUPS, 0 ].astype(int)

    def serial_predict(self, time_data):
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
        pdfs = np.vectorize(normal.pdf)
        points = time_period[valid_points[0]] - time_data
        index = np.argmax(pdfs(points))
        return valid_points[0][index]


def score(estimator, test_feat, test_labels):
    predictions = np.zeros(test_feat.shape[0], NUM_GROUPS)
    print("here")
    for i in range(test_feat.shape[0]):
        index = estimator.predict(test_feat[i,0])
        print(index)
        predictions[i,:] = estimator.labels[index]
    return np.mean(np.where(test_labels == predictions, 1, 0))


features, labels = get_all_data('TrainingData/training-50-users(1).csv')
x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=.2, random_state=42)

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

MEAN = 4.25
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
