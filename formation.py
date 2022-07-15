import pandas as pd
pd.options.mode.chained_assignment = None
import matplotlib.pyplot as plot
df=pd.read_csv('csv/HOBO_Master_40T_LR.csv')
df1=pd.read_csv('csv/HBEF_Kineo_wind_15min.csv')
df1['Date']=pd.to_datetime(df1['TIMESTAMP'])
df1['Time']=df1['Date'].dt.minute
df1.drop(df1.index[df1['Time']!=0], inplace=True)
df1.drop(df1.index[df1['TIMESTAMP']<'2013-05-19 23:00'], inplace=True)
df1.drop(df1.index[df1['TIMESTAMP']>'2020-08-10 07:00'], inplace=True)
df['WS_ms_Avg']=df1['WS_ms_Avg'].values
df['WS_ms_Max']=df1['WS_ms_Max'].values
df2=pd.read_csv('csv/Altered_Solar_Rad_data.csv')
df['Solar_Rad']=df2['solarrad'].values

# print(df)

# df.to_csv('formation dataframe.csv')
#below is gracies good code


##FIND INVERSIONS ###
a = df['slope'].values
print('a: ', a)  # a is an array with all the slopes
df['Start/End'] = ''
inversion = False
inv_count, inv_length=0, 0
i0, i_1, i_2, i_3 = 0, 0, 0, 0
df['invLen']=0
for i in range(0, len(a)):  # running through the entire data set
    i0 = a[i]
    try:  # setting temporary variables as the data ahead of i
        i_1 = a[i + 1]
        i_2 = a[i + 2]
        i_3 = a[i + 3]
    except:
        i_1, i_2, i_3 = a[-1], a[-1], a[-1]

    if not inversion:  # if there is not an inversion, check for one
        if i0 > 0 and i_1 > 0 and i_2 > 0:
            inv_count += 1
            df['invLen'][i] = 0
            inv_length += 1
            df['Start/End'][i] = 'Start'
            inversion = True

    elif inversion:  # if there is an inversion, check to see if it will dissipate
        inv_length += 1
        if i_1 < 0 and i_2 < 0 and i_3 < 0:
            df['invLen'][i+1] = inv_length
            inv_length = 0
            df['Start/End'][i + 1] = 'End'
            inversion = False
    #to this point, the entire data set has invLen and start/end, NOT +-6hours

df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month
df.to_csv('df.csv')

#for time series, locate the 6 hours before and after the inversion start/end, make new column for hours relative to inversion end time
df5 = pd.DataFrame()
df5['Hours from Start'] = ''
idx =''
for i in range(0, len(df)):
    if df['Start/End'][i] == 'Start':   # and df['invLen'][i]>0:
        j=i
        while df['invLen'][j]==0:
            j+=1
            inv_len=df['invLen'][j]
        if inv_len>=6:
            idx = df.index.get_loc(i)
            df5 = df5._append((df.iloc[idx - 6: idx + 7]))
            df5['Hours from Start'][idx - 6] = -6
            df5['Hours from Start'][idx - 5] = -5
            df5['Hours from Start'][idx - 4] = -4
            df5['Hours from Start'][idx - 3] = -3
            df5['Hours from Start'][idx - 2] = -2
            df5['Hours from Start'][idx - 1] = -1
            df5['Hours from Start'][idx] = 0
            df5['Hours from Start'][idx + 1] = 1
            df5['Hours from Start'][idx + 2] = 2
            df5['Hours from Start'][idx + 3] = 3
            df5['Hours from Start'][idx + 4] = 4
            df5['Hours from Start'][idx + 5] = 5
            df5['Hours from Start'][idx + 6] = 6

df5.drop(df5.index[df5['Month']==5], inplace=True)
df5.drop(df5.index[df5['Month']==6], inplace=True)
df5.drop(df5.index[df5['Month']==7], inplace=True)
df5.drop(df5.index[df5['Month']==8], inplace=True)
df5.drop(df5.index[df5['Month']==9], inplace=True)
df5.drop(df5.index[df5['Month']==10], inplace=True)

df5.to_csv('Cold_Inv_TimeSeries.csv')  ###Make into csv for memory purposes
print(df5)

fig, ax = plot.subplots()
ax.set_ylim(1.85,2.1)
ws=df5['WS_ms_Avg'].groupby(df5['Hours from Start'])
ax.plot(ws.mean(['WS_ms_Avg']))
plot.title("Kineo WS_Avg Inv Start")
plot.xlabel("hour")
plot.ylabel("wind speed (m/s)")
plot.show()
