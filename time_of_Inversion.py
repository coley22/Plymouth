# finding the frequency of time inversions per hour per month
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
df=pd.read_csv('csv/january.csv')
a=df['slope'].values
print('a: ',a)  # a is an array with all the slopes

new_df=pd.DataFrame()
inv_count=0
i3, i2, i1, i0, i_1, i_2=0,0,0,0,0,0
for i in range(0,len(a)):
    i0=a[i]
    if i==0 or i==1:
        i3, i2, i1 = a[0], a[0], a[0]
    elif i==2:
        i3, i2 = a[i-2], a[i-2]
        i1 = a[i-1]
    else:
        i3=a[i-3]
        i2=a[i-2]
        i1=a[i-1]
        try:
            i_1=a[i+1]
            i_2=a[i+2]
        except:
            i_1, i_2=a[-1], a[-1]

        if (i3>0 and i2>0 and i1>0 and i0<0) or (i3<0 and i2<0 and i1<0 and i0>0):
            if (i_1>0 and i_2>0 and i0>0) or (i_1<0 and i_2<0 and i0<0):
                inv_count+=1
                print('current count: ',inv_count)
                print("i3: ",i3)
                print("i2: ",i2)
                print("i1: ",i1)
                print("i0: ",i0,)
                print("i_1: ",i_1)
                print("i_2: ",i_2, '\n')
                new_df=new_df._append(df.iloc[[i]])


print('inversion count: ',inv_count)
new_df.to_csv('january hours with an inversion ND')

new_df['Date']=pd.to_datetime(new_df['Date'])
new_df['Time']=new_df['Date'].dt.hour
new_df.drop(new_df.index[new_df['slope']>0], inplace=True)  # dropping slopes with a positive/negative lapse rate
print(new_df)

# plotting frequency of all inversions in month by hour
y=(new_df['Time'].value_counts()/len(new_df['Time']))
y.sort_index(axis=0, ascending=True, inplace=True)  # **if an hour has 0 inversions, that hour is left off the x-axis**
y.plot(kind='bar', color='orange')
plot.title('Number of ** inversions by hour (January)')
plot.xlabel('time')
plot.ylabel('percentage of inversions')
plot.show()