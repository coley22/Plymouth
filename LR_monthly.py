import pandas as pd
import numpy as np
import matplotlib.pyplot as plot

# getting dates
df = pd.read_csv('HOBO_Master_40T_LR.csv')
# print(df)
# fucking january works now
# df = df[(df['Date'] >= ' 1/0/2013') & (df['Date'] <= '10/0/2019')]
# # df.to_csv('january.csv')
df = df[(df['Date'] >= '10/0/2013') & (df['Date'] <= '11/0/2020')]
print(df)
df.to_csv('october.csv')

# # day
# df['Date']=pd.to_datetime(df['Date'])
# df2=df.set_index('Date').between_time('09:00:00','22:00:00')
# df2.to_csv('january_day.csv')
#
# # night
# df['Date']=pd.to_datetime(df['Date'])
# df3=df.set_index('Date').between_time('23:00:00','08:00:00')
# df3.to_csv('january_night.csv')
#
# mean=df3['slope'].mean()    # CHANGE AS GRAPH CHANGES
# mean='{0:.3f}'.format(mean)
# mean=str(mean)
# mean_string='mean='+mean+'°C/km'
# print(mean_string)
#
# bins=range(-20,20)
# x=df3['slope']              # CHANGE AS GRAPH CHANGES
# plot.hist(x, weights=np.ones(len(x))/len(x), bins=bins)
#
# plot.title('January night')
# plot.ylabel('relative frequency')
# plot.xlabel('temperature gradient °C/km')
# plot.axvline(x=0, color='black', linestyle='--')
# plot.axvline(x=-9.8, color='red', linestyle='--')
# plot.text(7.4,.054, mean_string, fontsize=11)
# plot.show()
