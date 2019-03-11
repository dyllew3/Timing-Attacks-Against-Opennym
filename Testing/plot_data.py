import matplotlib.pyplot as plt
import numpy as np
num_users = int(input())

#all_data = np.genfromtxt("TrainingData/training-{}-users(3).csv".format(num_users), delimiter=',')
all_data = np.genfromtxt("TrainingData/ground_truth.csv", delimiter=',')

for i in range(num_users):
    threes = np.array(list(filter(lambda x: x[2] == i, list(all_data))))
    result = [np.array([threes[0,0], 0])]
    for subs in range(threes.shape[0] - 1):
        result.append(np.array([threes[subs + 1, 0], threes[subs + 1, 0] - threes[subs, 1]]))
    result = np.array(result)
    median = np.max(result[:,1])
    mu = np.mean(result[:, 1])
    sigma = np.std(result[:, 1])
    print('for {} mean is {} std is {}, max is {}'.format(i, mu, sigma, median))    
    s = np.random.normal(mu, sigma, 1000)
    #count, bins, p = plt.hist(result[:, 1], 20, density=True)
    plt.plot(result[:,0], result[:, 1], 'bo')
    #plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *  np.exp( - (bins - mu)**2 / (2 * sigma**2) ),       linewidth=3, color='y')
    plt.show()
