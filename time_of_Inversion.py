# finding the frequency of time inversions per hour per month
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
df=pd.read_csv('csv/july.csv')
a=df['slope'].values
u=np.sign(df['slope'])
m=np.flatnonzero(u.diff().abs().eq(2))
g=np.stack([m,m],axis=1)
v=np.abs(a[g].argmin(1))
df=df.iloc[g[np.arange(g.shape[0]),v]]
df['Date']=pd.to_datetime(df['Date'])
df['Time']=df['Date'].dt.hour
print(df)

# plotting frequency of all inversions in month by hour
y=df['Time'].value_counts()
y.sort_index(axis=0, ascending=True, inplace=True)
y.plot(kind='bar', color='orange')
plot.title('Number of inversions by hour (July)')
plot.xlabel('time')
plot.ylabel('# of inversions')
plot.show()