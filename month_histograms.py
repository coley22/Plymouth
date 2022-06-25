# gracie's code..

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#read in file and select only Jan dates
df = pd.read_csv('HOBO_Master_40T_LR.csv')

#extract a certain month from the master file
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month
df.drop(df.index[df['Month'] !=1], inplace=True) #drop all months besides the month you want to look at

#select only daytime values
df2 = df.set_index('Date').between_time('10:00:00','17:00:00')

# #make histogram of daytime temp gradients
ranges = range(-25, 25)
x = df2['slope']
fig,ax=plt.subplots(figsize=(7,5),dpi=100)
plt.hist(x, weights = np.ones(len(x))/len(x), bins = ranges)
plt.xlabel('Temperature Gradient (°C/km)')
plt.ylabel('Fraction of Temperature Gradients')
plt.title('January Daytime')
plt.axvline(x=0, color = 'black', linestyle = '--')
plt.axvline(x=-9.8, color = 'red', linestyle = '--')
mean = '{0:0.3}'.format(df2['slope'].mean())
mean = str(mean)
mean_string = 'mean=' +mean
plt.text(12,0.0665,mean_string, fontsize = 11)
count = str(len(df2))
count_string = 'n=' +count
plt.text(12,0.07,count_string, fontsize = 11)
plt.show

#select only nighttime values
df3 = df.set_index('Date').between_time('18:00:00','09:00:00')

#make histogram of nighttime temp gradients
x = df3['slope']
fig,ax=plt.subplots(figsize=(7,5),dpi=100)
plt.hist(x, weights = np.ones(len(x))/len(x), bins = ranges)
plt.xlabel('Temperature Gradient (°C/km)')
plt.ylabel('Fraction of Temperature Gradients')
plt.title('January Nighttime')
plt.axvline(x=0, color = 'black', linestyle = '--')
plt.axvline(x=-9.8, color = 'red', linestyle = '--')
mean = '{0:0.3}'.format(df3['slope'].mean())
mean = str(mean)
mean_string = 'mean=' +mean
plt.text(12,0.055 ,mean_string, fontsize = 11)
count = str(len(df3))
count_string = 'n=' +count
plt.text(12,0.05,count_string, fontsize = 11)
plt.show