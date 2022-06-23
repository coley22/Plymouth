# finding the frequency of time inversions per hour per month
import pandas as pd
import matplotlib.pyplot as plot
df=pd.read_csv('csv/August/august.csv')
a=df['slope'].values
print('a: ',a)  # a is an array with all the slopes

inversion=False
new_df=pd.DataFrame()
inv_count=0
i3, i2, i1, i0, i_1, i_2, i_3=0, 0, 0, 0, 0, 0, 0
for i in range(0, len(a)):
    i0=a[i]
    if i<=2:
        if i==0 or i==1:
            i3, i2, i1 = a[0], a[0], a[0]
        elif i==2:
            i3, i2 = a[i-2], a[i-2]
            i1 = a[i-1]
        i_1=a[i+1]
        i_2=a[i+2]
        i_3=a[i+3]
    else:
        i3=a[i-3]
        i2=a[i-2]
        i1=a[i-1]
        try:
            i_1=a[i+1]
            i_2=a[i+2]
            i_3=a[i+3]
        except:
            i_1, i_2, i_3 = a[-1], a[-1], a[-1]

    if not inversion:
        if i==0 and a[0]>0:
            print('Inversion began in previous month')
            inversion=True
        if (i3<0 and i2<0 and i1<0 and i0>0 and i_1>0 and i_2>0) or (i0>0 and i_1>0 and i_2>0):
            inv_count+=1
            print('Inversion',inv_count,'started at:', df.iloc[i][0], df.iloc[i][1], df.iloc[i][2])
            new_df=new_df._append(df.iloc[[i]])
            inversion=True
    elif inversion:
        if i==len(a):
            print('Inversion ended in the next month')
        if i_1<0 and i_2<0 and i_3<0:
            print('Inversion ended at: ', df.iloc[i][0], df.iloc[i+1][1], df.iloc[i+1][2], '\n')
            new_df=new_df._append(df.iloc[[i+1]])
            inversion = False


print('inversion count: ',inv_count)
new_df['Date']=pd.to_datetime(new_df['Date'])
new_df['Time']=new_df['Date'].dt.hour
# new_df.to_csv('csv/hours_with_inversion_master.csv')

# new_df.drop(new_df.index[new_df['slope']<0], inplace=True)  # dropping slopes with a positive/negative lapse rate
print(new_df)

# df=pd.read_csv('csv/hours_with_inversion_master.csv')
# df['Date']=pd.to_datetime(df["Date"])
# df['Month']=df['Date'].dt.month
# df.drop(df.index[df['Month']!=9], inplace=True)
# df.to_csv('csv/September/sep_inversion_hours.csv')
# print(df)


# plotting frequency of all inversions in month by hour
# y=(new_df['Time'].value_counts()/len(new_df['Time']))
# y.sort_index(axis=0, ascending=True, inplace=True)  # **if an hour has 0 inversions, that hour is left off the x-axis**
# y.plot(kind='bar', color='orange')
# plot.title('Number of positive inversions by hour (June)')
# plot.xlabel('time')
# plot.ylabel('percentage of inversions')
# plot.show()