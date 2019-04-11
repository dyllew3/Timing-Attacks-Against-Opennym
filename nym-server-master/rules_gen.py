from random import choice
from csv import writer, QUOTE_NONE

import string

with open('rules.csv', 'w', newline='') as input_file:
    header = ['id', 'domain', 'endpoint', 'rule']
    csv_writer = writer(input_file, quoting=QUOTE_NONE)
    csv_writer.writerow(header)
    n = 1800
    for i in range(n):
        # id,domain,endpoint,rule
        rule = ''.join(choice(string.ascii_uppercase + string.digits)
                       for _ in range(10))
        row = [i, 'spotify.com', 'localhost:4000', rule]
        csv_writer.writerow(row)
    pass
