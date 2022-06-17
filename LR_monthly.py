import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
from matplotlib.ticker import PercentFormatter

# getting dates
df = pd.read_csv('HOBO_Master_40T_LR.csv')
# print(df)
df = df[(df['Date'] >= '1/0/2014') & (df['Date'] <= '2/0/2020')]
print(df)
df.to_csv('shit_jan.csv')

# day
df['Date']=pd.to_datetime(df['Date'])
df2=df.set_index('Date').between_time('06:00:00','21:00:00')
# df2.to_csv('jan_day.csv')

#tr
# night
df['Date']=pd.to_datetime(df['Date'])
df3=df.set_index('Date').between_time('21:00:00','06:00:00')
# df3.to_csv('jan_night.csv')

mean=df['slope'].mean()


bins = range(-20,20)
x = df['slope']
plot.hist(x, weights=np.ones(len(x))/len(x), bins=bins)

# plot.gca().yaxis.set_major_formatter(PercentFormatter(1))
plot.title('January only day')
plot.ylabel('relative frequency')
plot.xlabel('temperature gradient')
# plot.xticks(bins)
plot.axvline(x=0, color='black')
plot.axvline(x=mean, color='red')

# plot.show()
