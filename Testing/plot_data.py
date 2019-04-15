import matplotlib.pyplot as plt
import numpy as np
import csv

num_users = 100

all_data = np.genfromtxt("TrainingData/training-{}-users.csv".format(num_users), delimiter=',')
#all_data = np.genfromtxt("TrainingData/ground_truth.csv", delimiter=',')


mean_of_means = 0
mean_of_stds = 0

with open('Results/mean_std_linear_reg.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',' )
    writer.writerow(['Distance', 'Mean', 'Std'])
    for back in range(1, 731):
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
        print(np.array(overall).shape)
        std = np.std(np.array(overall)[:,1])
        #print(total/length)
        writer.writerow([back, mean, std])
        #print(mean_of_stds/num_users)
        #print(np.std(np.array(overall)[:,1]))



