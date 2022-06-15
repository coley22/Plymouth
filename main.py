import pandas
import numpy
import matplotlib.pyplot as plot
import csv
from matplotlib.ticker import PercentFormatter

# WE NEED THE LOWEST 21 LAPSE RATES, BUT ALL 40 MAX TEMPERATURES
# so, if there was an inversion present at one of the lowest 21 loggers, we need the maxT for that hour, regardless of elevation

data=pandas.read_csv('new_Histogram_Data.csv')
data.drop(data.index[data['lapseRate']<=0], inplace=True)
data=data[data['lapseRate'].notna()]
# dropping the lowest 3 sensors
data.drop(data.index[data['elevation']<350], inplace=True)

# at this point, we have a dataframe with all the hours with a positive lapse rate
# going to attempt to remove rows of data with an elevation greater than 613m (WS1)
# data.drop(data.index[data['elevation']>613], inplace=True)
print(data)
data.to_csv('filtered_LR.csv', index=False)


bins_data=pandas.read_csv('filtered_LR.csv')
bins=[300,350,400,450,500,550,600,650,700,750,800,850,900]
plot.hist(bins_data.elevation, weights=numpy.ones(len(bins_data.elevation))/len(bins_data.elevation), bins=bins)
plot.gca().yaxis.set_major_formatter(PercentFormatter(1))
plot.xticks(bins)
plot.xlabel('Elevation(m)')
plot.ylabel('Percent(%)')
plot.title('Frequency of Max Temperature Occurrence')
plot.show()



# output = open('positive_lapse_Rate.csv', 'w')
# output_header="Date,slope\n"
# output.write(output_header)
#
# positive_count=0
#
# with open('new_Histogram_Data.csv') as infile:
#     reader = csv.reader(infile, delimiter=',')
#     header = next(reader)
#     print(header[1])
#     for row in reader:
#         value_length = len(row[1])
#         print(row)
        # if value_length>0:
        #     lapse_rate = float(row[1])
        #     # print(value_length)
        #     if lapse_rate<0:
        #         # print(row[0], lapse_rate)
        #         positive_count+=1
#                 file_input = "{},{}\n".format(row[0],lapse_rate)
#                 # going to write ALL the positive lapse rates to a file
#                 # still must exclude data from above the 21 lowest sites
#                 # still must exclude max observations from 3 lowest stations
#                 output.write(file_input)
# output.close()
