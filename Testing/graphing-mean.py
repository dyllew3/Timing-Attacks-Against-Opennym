import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

x_vals = [1,2,5]#,10,25,50,100]
active_users = [1, 2, 5, 10, 25, 50, 75, 100, 125, 150]
ind = np.arange(1, 150)


def get_all_data(filename,delimiter=','):
    all_data = np.genfromtxt(filename, delimiter=delimiter)
    return all_data[1:]
b = get_all_data('Results/mean_std.csv')

vals = [1, 2, 5, 10, 25, 50, 100]
active_users = b[:, 0]
group_1 = b[:, 2]

from sklearn.model_selection import train_test_split  
X_train, X_test, y_train, y_test = train_test_split(active_users, group_1, test_size=0.2, random_state=0)

from sklearn.linear_model import LinearRegression  
regressor = LinearRegression()  
regressor.fit(X_train.reshape(-1, 1), y_train)
print(regressor.intercept_)
print(regressor.coef_)

y_pred = regressor.predict(X_test.reshape(-1, 1))
from sklearn import metrics  
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))  
#group_1_err = (b[np.where(b[:,1] == val)])[:len(active_users),3]

plt.xlabel('Space between Rating Update Requests')
plt.ylabel('Standard Deviation')
plt.plot(active_users, group_1, color='green', marker='.', linestyle="dashed")

#plt.xticks(ind, ('1', '2', '5', '10', '50', '75', '100'))
#plt.xticks(range(0, 160, 10))
#plt.yticks(np.arange(0, 1.1, step=0.1))

plt.grid()
plt.savefig('Results/std.png')
plt.show()


import seaborn as sns
from scipy import stats