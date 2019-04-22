import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

dummy_percents = [10, 20, 40, 60, 80]
x_vals = [1, 2 ]#, 10, 25, 50, 100]
active_users = [1, 2, 5, 10, 50, 75, 100]
ind = np.arange(1, 100)

def get_real_amount(users_arr, percent):
    result = []
    for user in users_arr:
        result.append(user - (user*percent) // 100)
    return result

def get_all_data(filename,delimiter=','):
    all_data = np.genfromtxt(filename, delimiter=delimiter)
    return all_data[1:]
b = get_all_data('Results/baseline-grouping-application-layer-latency.csv')

users_1 = (b[np.where(b[:,0] == 1)])[:len(x_vals),2]
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

vals = [1]#, 2, 5, 10, 25, 50, 100]
#real_users = get_real_amount(active_users, dummy_percent)
with open('Results/Application Layer/dummy-defence.csv', 'r', newline='') as csvfile:
	#header = ['Group Size', 'Number of Real Users', 'Number of Dummy Users', 'Percentage of Dummy Users', 'Accuracy']
	#csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, delimiter=',')
	#csv_writer.writerow(header)
	for val in vals :
		group_1 = (b[np.where(b[:,1] == val)])[:len(active_users),2]
		group_1_err = (b[np.where(b[:,1] == val)])[:len(active_users),3]
		#for dummy_percent in dummy_percents:
			#for i in range(len(active_users)):
			#	real_user = active_users[i] - (active_users[i]*dummy_percent)//100
			#	csv_writer.writerow([val, real_user,  (active_users[i]*dummy_percent)//100, dummy_percent, group_1[i]])
			#fig = plt.figure()
			#ax = plt.subplot()
			#real_users = get_real_amount(active_users, dummy_percent)
			#x_vals = get_real_amount(active_users, dummy_percent)
			## Data
			#df=pd.DataFrame({
			#	'x': x_vals,
			#	'{} \'real\' Active User'.format(x_vals[0]): users_1,
			#	'{} \'real\' Active Users'.format(x_vals[1]): users_2,
			#	'{} \'real\' Active Users'.format(x_vals[2]): users_5,
			#	'{} \'real\' Active Users'.format(x_vals[3]): users_10,
			#	'{} \'real\' Active Users'.format(x_vals[4]): users_50,
			#	'{} \'real\' Active Users'.format(x_vals[5]): users_75,
			#	'{} \'real\' Active Users'.format(x_vals[6]): users_100
			#	})
#
#
#
			## multiple line plot
			#ax.plot( 'x', '{} \'real\' Active User'.format(x_vals[0]), data=df, marker='', color='skyblue', linewidth=2)
			#ax.plot( 'x', '{} \'real\' Active Users'.format(x_vals[1]), data=df, marker='', color='red', linewidth=2)
			#ax.plot( 'x', '{} \'real\' Active Users'.format(x_vals[2]), data=df, marker='', color='green', linewidth=2, linestyle='dashed')
			#ax.plot( 'x', '{} \'real\' Active Users'.format(x_vals[3]), data=df, marker='', color='orange', linewidth=2)
			#ax.plot( 'x', '{} \'real\' Active Users'.format(x_vals[4]), data=df, marker='', color='purple', linewidth=2, linestyle='dashed')
			#ax.plot( 'x', '{} \'real\' Active Users'.format(x_vals[5]), data=df, marker='', color='olive', linewidth=2)
			#ax.plot( 'x', '{} \'real\' Active Users'.format(x_vals[6]), data=df, marker='', color='black', linewidth=2, linestyle='dashed')
			#plt.xlabel('Group size')
			#plt.ylabel('Accuracy')
#
#
			#box = ax.get_position()
			#ax.set_position([box.x0, box.y0 + box.height * 0.1,
			#				box.width, box.height * 0.9])
#
			## Put a legend below current axis
			#ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
			#		fancybox=True, shadow=True, ncol=5)
		plt.xlabel('Number of active users')
		plt.ylabel('Accuracy')
		width = 0.35
		plt.errorbar(active_users, group_1, yerr=group_1_err, color='red', ecolor='black', fmt='--o')
		#plt.xticks(ind, ('1', '2', '5', '10', '50', '75', '100'))
		plt.xticks(range(0, 105, 5))
		plt.yticks(np.arange(0, 1.1, step=0.1))
		plt.grid()

		plt.savefig('Results/Application Layer/grouping-{}-latency.png'.format(val))
		plt.show()
