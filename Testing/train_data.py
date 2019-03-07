import numpy as np
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn import neighbors, datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import MiniBatchKMeans
from sklearn.ensemble import AdaBoostClassifier
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras

vector_size = 3
def normalise_data(x):
      # rescale data to lie between 0 and 1
  scale = x.max(axis=0)
  return x/scale

def get_all_data(filename,delimiter=','):
    all_data = np.genfromtxt(filename, delimiter=delimiter)
    # Randomly sample from the input file if it is for testing data
    features = all_data[:, :-1]
    new_features = np.zeros((features.shape[0], vector_size))
    amount = int(new_features.shape[0] * 0.8)
    labels = all_data[:, all_data.shape[1] - 1].ravel()
    for i in range(features.shape[0]):
        index = i
        if i > (vector_size):
            new_features[index] = np.abs(((features[i - (vector_size + 1):i-1,1] - features[i,0])))
            pass
        else:
            empty_vec = np.zeros(vector_size)
            empty_vec[:i] = features[:i,1]
            new_features[i] = np.abs(empty_vec)
    features = (new_features)
    #labels = labels[(vector_size + 1):]
    return features, labels    

def get_data(filename,delimiter=','):
    all_data = np.genfromtxt(filename, delimiter=delimiter)
    # Randomly sample from the input file if it is for testing data
    features = all_data[:, :-1]
    new_features = np.zeros((features.shape[0], vector_size))
    amount = int(new_features.shape[0] * 0.8)
    labels = all_data[:, all_data.shape[1] - 1].ravel()
    for i in range(features.shape[0]):
        index = i
        if i > (vector_size):
            new_features[index] = np.abs(((features[i - (vector_size + 1):i-1,1] - features[i,0])))
            pass
        else:
            empty_vec = np.zeros(vector_size)
            empty_vec[:i] = np.abs(features[:i,1])
            new_features[i] = empty_vec
    features = (new_features)
    #labels = labels[(vector_size + 1):]
    return (features[:amount, :] , labels[:amount]), (features[amount:, :], labels[amount:])


C = 0.75  # SVM regularization parameter

(x_train, y_train), (x_test, y_test) = (get_data('TrainingData/training-5-users.csv'))

clf = svm.SVC(gamma='auto',decision_function_shape='ovo',class_weight='balanced')
clf.fit(x_train, y_train)
print(clf.score(x_test, y_test))

clf = LinearSVC(random_state=0, tol=1e-5)
clf.fit(x_train, y_train)
print("Linear SVC")
print(clf.score(x_test, y_test))

n_neighbors = 5

for weights in ['uniform','distance']:
    # we create an instance of Neighbours Classifier and fit the data.
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
    clf.fit(x_train, y_train)
    print("Nearest neighbour")
    print(clf.score(x_test, y_test))

clf = RandomForestClassifier(n_estimators=20)
clf.fit(x_train, y_train)
print("Ensemble classifier")
print(clf.score(x_test, y_test))

from sklearn.model_selection import cross_val_score
print("Adabooster")
clf = AdaBoostClassifier(n_estimators=100)
scores = cross_val_score(clf, x_train, y_train, cv=10)
print(scores.mean())

from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.partial_fit(x_train, y_train, classes=np.arange(50))
print("Guassian NB")
print(clf.score(x_test, y_test))

from sklearn.naive_bayes import ComplementNB
clf = ComplementNB()
clf.fit(x_train, y_train)
print("Complement NB")
print(clf.score(x_test, y_test))

from sklearn.neighbors.nearest_centroid import NearestCentroid
clf = NearestCentroid(shrink_threshold=0.2)
clf.fit(x_train, y_train)
print("Nearest Centroid")
print(clf.score(x_test, y_test))

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.neighbors import NearestCentroid

h = .02  # step size in the mesh

# Create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF', '#AAAAAA', '#FFAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF', '#000000', '#FF00FF'])

for shrinkage in [None, .2]:
    X, y = x_train, y_train
    # we create an instance of Neighbours Classifier and fit the data.
    clf = NearestCentroid(shrink_threshold=shrinkage)
    clf.fit(X, y)
    y_pred = clf.predict(X)
    print(shrinkage, np.mean(y == y_pred))
    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    z_min, z_max = X[:, 2].min() - 1, X[:, 2].max() + 1
    xx, yy, zz = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h),
                         np.arange(z_min, z_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel(), zz.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure().add_subplot(111, projection='3d')

    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1],X[:, 2], c=y, cmap=cmap_bold,
                edgecolor='k', s=20)
    plt.title("3-Class classification (shrink_threshold=%r)"
              % shrinkage)
    plt.axis('tight')

    plt.show()




from sklearn.metrics import brier_score_loss
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split


X, y = get_all_data('TrainingData/training-5-users.csv')

sample_weight = np.random.RandomState(42).rand(y.shape[0])

X_train, X_test, Y_train, Y_test, sw_train, sw_test = \
    train_test_split(X, y, sample_weight, test_size=0.2, random_state=42)

clf = GaussianNB()
clf.fit(X_train, Y_train)  # GaussianNB itself does not support sample-weights
prob_pos_clf = clf.predict_proba(X_test)[:, 1]

# Gaussian Naive-Bayes with isotonic calibration
clf_isotonic = CalibratedClassifierCV(clf, cv=5, method='isotonic')
clf_isotonic.fit(X_train, Y_train, sw_train)
prob_pos_isotonic = clf_isotonic.predict_proba(X_test)[:, 1]

# Gaussian Naive-Bayes with sigmoid calibration
clf_sigmoid = CalibratedClassifierCV(clf, cv=5, method='sigmoid')
clf_sigmoid.fit(X_train, Y_train, sw_train)
print(clf_sigmoid.score(X_test, Y_test))
prob_pos_sigmoid = clf_sigmoid.predict_proba(X_test)[:, 1]

print("Brier scores: (the smaller the better)")

clf_score = brier_score_loss(Y_test, prob_pos_clf, sw_test)
print("No calibration: %1.3f" % clf_score)

clf_isotonic_score = brier_score_loss(Y_test, prob_pos_isotonic, sw_test)
print("With isotonic calibration: %1.3f" % clf_isotonic_score)

clf_sigmoid_score = brier_score_loss(Y_test, prob_pos_sigmoid, sw_test)
print("With sigmoid calibration: %1.3f" % clf_sigmoid_score)

from sklearn import tree
clf = tree.DecisionTreeClassifier()
clf.fit(x_train, y_train)
print("Decision Tree")
print(clf.score(x_test, y_test))

plt.show()
#main()

from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(solver='liblinear',multi_class='ovr',fit_intercept=False,class_weight='balanced').fit(x_train, y_train)
print('Logistical Regression')
print(clf.score(x_test, y_test))

from sklearn.naive_bayes import BernoulliNB
clf = BernoulliNB(alpha=0.00001)
clf.fit(x_train, y_train)
print("Bernoulli Random variable")
print(clf.score(x_test, y_test))