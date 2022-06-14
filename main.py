# this script takes the lapse rate file and filters out the positive lapse rates and writes them to a new file

import pandas as panda
import numpy as np
import matplotlib.pyplot as plot
import csv

output = open('positive_lapse_Rate.csv', 'w')
output_header="Date,slope\n"
output.write(output_header)

positive_count=0

with open('HBEF_lapse_rates.csv', 'r') as infile:
    reader = csv.reader(infile, delimiter=',')
    header = next(reader)
    print(header[1])
    for row in reader:
        value_length = len(row[1])
        if value_length>0:
            lapse_rate = float(row[1])
            # print(value_length)
            if lapse_rate<0:
                # print(row[0], lapse_rate)
                positive_count+=1
                file_input = "{},{}\n".format(row[0],lapse_rate)
                # going to write ALL the positive lapse rates to a file
                # still must exclude data from above the 21 lowest sites
                # still must exclude max observations from 3 lowest stations
                output.write(file_input)
output.close()


print("# of hours with positive lapse rate: ",positive_count)
print("hey")
# could modidfy hobo_inversions script to also give the max temperature
# could make a script to edit the master T before running hobo_inversion to eliminate higher elevation sites








# data=panda.read_csv('HBEF_lapse_rates.csv')
# print(data)
# for hobo in data:
#     if hobo == 'Temp005':
#         plot.plot(data['Date'], data['Temp005'])

        #code that picks out the positive slopes(?) and plots them based on elevation
# plot.hist(data.slope)
# plot.show()