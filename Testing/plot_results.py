import matplotlib.pyplot as plt
import numpy as np

all_data = np.genfromtxt("Results/baseline-ip-layer.csv", delimiter=',')


x = all_data[1:,0]
y = all_data[1:,1]
e = all_data[1:,2]

plt.errorbar(x, y, e, linestyle='None', marker='.')

plt.show()