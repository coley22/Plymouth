####  This code computes a linear regression and a 4th order polynominal 
##      regression through all HBEF HOBO sites for each hour.
# """
# Created on Mon Jun 28 21:48:49 2021 by Eric Kelsey
# """
import pandas as pd
import numpy as np
import csv
from scipy import stats
from scipy.optimize import minimize

output=open('csv/Histogram_Data.csv', 'w')
output_header="Date,maxT,logger,elevation\n"
output.write(output_header)

# cleaning up the data in 'HOBO_Master_T'
with open('HOBO_Master_T.csv') as infile:
    reader = csv.reader(infile, delimiter=',')
    # taking the loggers and their elevations and putting them into arrays with matching indices
    logger = next(reader)
    logger.pop(0)
    elevations = next(reader)
    elevations.pop(0)
    elevations = list(map(float, elevations))
    logger2 = logger.copy()
    elevations2 = elevations.copy()

    # removing column headings (logger, elevation) if there is missing data
    for row in reader:
        date = row.pop(0)
        i=-1
        for x in row[:]:
            i+=1
            if x == "":
                row.remove(x)
                a=logger.pop(i)
                b=elevations.pop(i)
                i-=1
        # casting the temperature values to floats
        row = list(map(float, row))
        # print(logger[15], elevations[15], row[15])

        # finding the max temperature in each row and finding that index
        max_temp = max(row)
        max_temp_index = row.index(max_temp)

        file_input=file_input = "{},{},{},{}\n".format(date, max_temp, logger[max_temp_index], elevations[max_temp_index])
        output.write(file_input)
        # print(date, max_temp, logger[max_temp_index], elevations[max_temp_index])
        logger = logger2.copy()
        elevations = elevations2.copy()
output.close()


# kelsey's code
fin = pd.read_csv('HOBO_Master_T.csv')
fin1 = pd.read_csv('HOBO_Elevations.csv')

fin.index = pd.to_datetime(fin.Date)
fin = fin.drop(['Date'], axis=1)
lapserates = pd.DataFrame(np.nan, index=fin.index, columns=['slope'])
num_count = fin.count(axis=1)
x=0

analysistype = input("Do you want to calculate a linear regression for each hour? (yes/no):\n")
if analysistype == "yes":
    for i in range(len(fin)):
        # print(fin[i])
        if num_count[i] >= 30:
            z = (fin.iloc[i] > -40)
            slope, intercept, r, p, se = stats.linregress(fin1['meanElev'][z.values], fin.iloc[i][z])
            lapserates.at[fin.index[i],'slope'] = slope*1000
        elif num_count[i] < 30:
            x = x+1

print('number of hours with insufficient HOBOs = '+str(x))
print('percent of hours with insufficient HOBOs = '+str(x/len(fin)*100)+'%')
lapserates.to_csv(r'HBEF_lapse_rates.csv', index=True)

analysistype2 = input("Do you want to calculate a polynomial regression for each hour? (yes/no):\n")
if analysistype2 == "yes":
    coeff_array = pd.DataFrame()
    for i in range(5):#range(len(fin)):
        z = (fin.iloc[i] > -40)
        coeff = np.polyfit(fin1['meanElev'][z.values], fin.iloc[i][z],4)
        coeff = pd.DataFrame(coeff)
        coeff_array = pd.concat([coeff_array,coeff],axis=1)

coeff_array = coeff_array.T
