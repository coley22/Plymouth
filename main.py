import pandas
import numpy
import matplotlib.pyplot as plot
import csv
from matplotlib.ticker import PercentFormatter

# WE NEED THE LOWEST 21 LAPSE RATES, BUT ALL 40 MAX TEMPERATURES
# so, if there was an inversion present at one of the lowest 21 loggers, we need the maxT for that hour, regardless of elevation

# data=pandas.read_csv('new_Histogram_Data.csv')
# data.drop(data.index[data['lapseRate']<=0], inplace=True)
# data=data[data['lapseRate'].notna()]
# # dropping the lowest 3 sensors
# data.drop(index=data.index[data['elevation']<350], inplace=True)
# # at this point, we have a dataframe with all the hours with a positive lapse rate
# # going to attempt to remove rows of data with an elevation greater than 613m (WS1)
# data.drop(data.index[data['elevation']>613], inplace=True)
# print(data)
# data.to_csv('filtered_LR.csv', index=False)


# now what I will attempt to do is use the csv with the hours a positive inversion was present in the lowest 21
#   loggers to find the maxT and elevation at that hour

hours=pandas.read_csv('filtered_LR.csv')
dates_needed=hours.iloc[:,0] #works
# print("dates needed:\n",dates_needed, "\n")
dates_needed_list=dates_needed.tolist()

print(dates_needed_list)

bto=pandas.read_csv('HOBO_Master_T.csv')
bto_dates=bto.iloc[:,0]    #grabbing the dates to compare with dates_needed
bto_dates.drop(index=bto_dates.index[0], inplace=True)  #dropping NaN index
# print("bto dates:\n",bto_dates,"\n")
bto.drop(columns=bto.columns[0], axis=1, inplace=True)  #dropping the dates index
# print("bto: \n",bto)
# print(dates_needed[0], bto_dates[1])    # bto_dates needs to be an index ahead of dates_needed

count=0
for i in range (1, len(bto_dates)): # THERE IS AN OFF BY 1 ERROR
    a=bto_dates[i]
    if a in dates_needed_list:
        # print(a)
        # find max T in HOBO master
        max_T=bto.max(axis=1)
        # print(max_T)
        count+=1
print("dates identified: ",count)



# histogram
# bins_data=pandas.read_csv('filtered_LR.csv')
# bins=[300,350,400,450,500,550,600,650,700,750,800,850,900]
# plot.hist(bins_data.elevation, weights=numpy.ones(len(bins_data.elevation))/len(bins_data.elevation), bins=bins)
# plot.gca().yaxis.set_major_formatter(PercentFormatter(1))
# plot.xticks(bins)
# plot.xlabel('Elevation(m)')
# plot.ylabel('Percent(%)')
# plot.title('Frequency of Max Temperature Occurrence')
# plot.show()



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
