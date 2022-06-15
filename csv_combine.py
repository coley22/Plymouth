# essentially combining the histogram data and the lapse rates into a new csv
import csv
import pandas

# taking the lapse rates and copying them to an array
rates=[]
with open('HBEF_lapse_rates.csv') as infile:
    reader = csv.reader(infile)
    for row in reader:
        rat=row.pop(1)
        rates.append(rat)
    # print(rates[:4])
    rates.pop(1)
    rates.pop(0)
    print(rates[:4])

# adding the lapse rates to a new column in 'Histogram_Data'
df=pandas.read_csv('Histogram_Data.csv')
df['lapseRate']=rates
print(df)
df.to_csv('new_Histogram_Data.csv', index=False)
