import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

x_vals = [1,2,5]#,10,25,50,100]
active_users = [1, 2, 5, 10, 50, 75, 100]
ind = np.arange(1, 8)


def get_all_data(filename,delimiter=','):
    all_data = np.genfromtxt(filename, delimiter=delimiter)
    return all_data[1:]
b = get_all_data('Results/baseline-grouping-application-layer.csv')

"""users_1 = (b[np.where(b[:,0] == 1)])[:len(x_vals),2]
users_1_err = (b[np.where(b[:,0] == 1)])[:len(x_vals),3]

users_2 =  (b[np.where(b[:,0] == 2)])[:len(x_vals),2]
users_2_err = (b[np.where(b[:,0] == 2)])[:len(x_vals),3]

users_5 =  (b[np.where(b[:,0] == 5)])[:len(x_vals),2]
users_5_err = (b[np.where(b[:,0] == 5)])[:len(x_vals),3]

users_10 = (b[np.where(b[:,0] == 10)])[:len(x_vals),2]
users_10_err = (b[np.where(b[:,0] == 10)])[:len(x_vals),3]

users_50 = (b[np.where(b[:,0] == 50)])[:len(x_vals),2]
users_50_err = (b[np.where(b[:,0] == 50)])[:len(x_vals),3]

users_75 = (b[np.where(b[:,0] == 75)])[:len(x_vals),2]
users_75_err = (b[np.where(b[:,0] == 75)])[:len(x_vals),3]

users_100 = (b[np.where(b[:,0] == 100)])[:len(x_vals),2]
users_100_err = (b[np.where(b[:,0] == 100)])[:len(x_vals),3]
"""
group_1 = (b[np.where(b[:,1] == 50)])[:len(active_users),2]
group_1_err = (b[np.where(b[:,1] == 50)])[:len(active_users),3]
print(group_1)

fig = plt.figure()
ax = plt.subplot()

"""
# Data
df=pd.DataFrame({
    'x': x_vals,
    '1 Active User': users_1,
    '2 Active Users': users_2,
    '5 Active Users': users_5,
    '10 Active Users': users_10,
    '50 Active Users': users_50,
    '75 Active Users': users_75,
    '100 Active Users': users_100
    })



# multiple line plot
ax.plot( 'x', '1 Active User', data=df, marker='', color='skyblue', linewidth=2)
ax.plot( 'x', '2 Active Users', data=df, marker='', color='red', linewidth=2)
ax.plot( 'x', '5 Active Users', data=df, marker='', color='green', linewidth=2, linestyle='dashed')
ax.plot( 'x', '10 Active Users', data=df, marker='', color='orange', linewidth=2)
ax.plot( 'x', '50 Active Users', data=df, marker='', color='purple', linewidth=2, linestyle='dashed')
ax.plot( 'x', '75 Active Users', data=df, marker='', color='olive', linewidth=2)
ax.plot( 'x', '100 Active Users', data=df, marker='', color='black', linewidth=2, linestyle='dashed')
plt.xlabel('Group size')
plt.ylabel('Accuracy')


box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
          fancybox=True, shadow=True, ncol=5)
plt.savefig('Results/grouping.png')"""
plt.xlabel('Amount of active users')
plt.ylabel('Accuracy')
width = 0.35
plt.bar(ind, group_1, width, yerr=group_1_err)
plt.xticks(ind, ('1', '2', '5', '10', '50', '75', '100'))

plt.savefig('Results/grouping-50.png')
plt.show()

