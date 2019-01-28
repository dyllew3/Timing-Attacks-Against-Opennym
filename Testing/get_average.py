import numpy as np
from numpy import genfromtxt
import csv

def time_diff_update(array):
    result = []
    i = 1
    arr_len = len(array)
    while i + 2 < arr_len:
        if array[i][6] == "Application Data":
            sent_diff = float(array[i + 1][1]) - float(array[i][1])
            second_diff = float(array[i + 2][1]) - float(array[i][1])
            third_diff = float(array[i + 2][1]) - float(array[i + 1][1])
            result.append([sent_diff, second_diff, third_diff])
            i += 3
        else:
            i += 1
    return result



def get_time_diff(array):
    result = []
    i = 1
    arr_len = len(array)
    while i + 1 < arr_len:
        if array[i][6] == "Application Data":
            result.append((float(array[i + 1][1]) - float(array[i][1])))
            i += 2
        else:
            i += 1
    return result

with open('Timing-Operations-Results/12-Rules-Issued-Domain.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    rows = []
    for row in spamreader:
        rows.append(row)
    al = np.array(time_diff_update(rows))
    print('\n'.join([str(x) for x in al]))
    print("Average is {}".format(np.mean(al, axis=0)))
    print("Median is {}".format(np.median(al, axis=0)))