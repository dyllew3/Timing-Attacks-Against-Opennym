import matplotlib.pyplot as plt
import numpy as np
num_users = 100

all_data = np.genfromtxt("TrainingData/training-{}-users.csv".format(num_users), delimiter=',')
#all_data = np.genfromtxt("TrainingData/ground_truth.csv", delimiter=',')

total = 0
length = 0
mean_of_means = 0
mean_of_stds = 0
overall = []
for i in range(num_users):
    threes = np.array(list(filter(lambda x: x[2] == i, list(all_data))))
    result = [np.array([threes[0,0], 0])]
    back = 8
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
    #print('for {} mean is {} std is {}, max is {}'.format(i, mu, sigma, median))    
    s = np.random.normal(mu, sigma, 1000)
    #count, bins, p = plt.hist(result[:, 1], 20, density=True)
    plt.plot(result[:,0], result[:, 1], 'bo')
    #plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *  np.exp( - (bins - mu)**2 / (2 * sigma**2) ),       linewidth=3, color='y')
    #plt.show()

print(total/length)
#print(mean_of_stds/num_users)
print(np.std(np.array(overall)[:,1]))
