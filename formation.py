import pandas as pd
df=pd.read_csv('csv/HOBO_Master_40T_LR.csv')
df1=pd.read_csv('HBEF_Kineo_wind_15min.csv')
df1['Date']=pd.to_datetime(df1['TIMESTAMP'])
df1['Time']=df1['Date'].dt.minute
df1.drop(df1.index[df1['Time']!=0], inplace=True)
df1.drop(df1.index[df1['TIMESTAMP']<'2013-05-19 23:00'], inplace=True)
df1.drop(df1.index[df1['TIMESTAMP']>'2020-08-10 07:00'], inplace=True)
# print(df1)

df['WS_ms_Avg']=df1['WS_ms_Avg'].values
df['WS_ms_Max']=df1['WS_ms_Max'].values
df2=pd.read_csv('Solar_Rad_Data.csv')
print(df2)
df['Solar_Rad']=df2['Solar Rad'].values

print(df)







# a=df['slope'].values
# print('a: ',a)  # a is an array with all the slopes
#
# inversion=False
# new_df=pd.DataFrame()
# inv_count, inv_length=0, 0
# i0, i_1, i_2, i_3 = 0, 0, 0, 0
# new_df['invLen']=0
#
# for i in range(0, len(a)):  # running through the entire data set
#     i0=a[i]
#     try:    # setting temporary variables as the data ahead of i
#         i_1=a[i+1]
#         i_2=a[i+2]
#         i_3=a[i+3]
#     except:
#         i_1, i_2, i_3 = a[-1], a[-1], a[-1]
#
#     if not inversion:   # if there is not an inversion, check for one
#         if i0>0 and i_1>0 and i_2>0:
#             inv_count+=1
#             print('Inversion',inv_count,'started at:', df.iloc[i][0], df.iloc[i][1])
#             new_df=new_df._append(df.iloc[[i]])
#             new_df.at[i,['invLen']]=0
#             inv_length += 1
#             inversion=True
#     elif inversion: # if there is an inversion, check to see if it will dissipate
#         inv_length+=1
#         if i_1<0 and i_2<0 and i_3<0:
#             print('Inversion ended at: ', df.iloc[i+1][0], df.iloc[i+1][1], '\n')
#             new_df=new_df._append(df.iloc[[i+1]])
#             new_df.at[i+1,['invLen']]=inv_length
#             inv_length = 0
#             inversion = False
#
# print('inversion count: ',inv_count)
# new_df['Date']=pd.to_datetime(new_df['Date'])
# new_df['Time']=new_df['Date'].dt.hour
# new_df['Month']=new_df['Date'].dt.month
# new_df.to_csv('csv/hours_with_inversion_master2.csv')    # a csv with all the hours with an inversion
# print(new_df)