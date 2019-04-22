import matplotlib.pyplot as plt
import numpy as np
import csv
import seaborn as sns
num_users = 2

all_data = np.genfromtxt("TrainingData/training-{}-users.csv".format(num_users), delimiter=',')
#all_data = np.genfromtxt("TrainingData/ground_truth.csv", delimiter=',')


mean_of_means = 0
mean_of_stds = 0

"""
back = 1
print(back)
total = 0
length = 0
overall = []
for i in range(num_users):
    threes = np.array(list(filter(lambda x: x[2] == i, list(all_data))))
    result = [np.array([threes[0,0], 0])]
    for subs in range(threes.shape[0] - back):
        result.append(np.array([threes[subs + back, 0], threes[subs + back, 0] - threes[subs, 1]]))
        overall.append(np.array([threes[subs + back, 0], threes[subs + back, 0] - threes[subs, 1]]))
    result = np.array(result)
    total += np.sum(result[:, 1])
    length += threes.shape[0]
    median = np.max(result[:,1])
    mu = np.mean(result[:, 1])
    mean_of_means += mu
    sigma = np.std(result[:, 1])
    mean_of_stds += sigma
mean = total/length
print(total/length)
#sns.set(color_codes=True)
sns.set(); np.random.seed(0)
x = np.random.randn(100)
ax = sns.distplot(np.array(overall)[:, 1], hist=True, kde=False)
ax.set(xlabel='Time Difference Between Rating Updates', ylabel='Frequency')
std = np.std(np.array(overall)[:,1])
plt.show()
#print(total/length)
#print(mean_of_stds/num_users)
#print(np.std(np.array(overall)[:,1]))
"""
user_0 = all_data[np.where(all_data[:, 2] == 0)]
user_1 = all_data[np.where(all_data[:, 2] == 1)]

x_user0 = user_0[:10, 0]
y_user0 = user_0[:10, 2]

x_user1 = user_1[:10, 0]
y_user1 = user_0[:10, 2]
#print(x_user0)

plt.figure()
plt.subplot()
plt.xlabel('Time From Start (Minutes)')
plt.plot(x_user0, y_user0, 'bo', x_user1, y_user1, 'go')
plt.show()
