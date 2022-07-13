# finding the frequency of time inversions per hour per month
import pandas as pd
import matplotlib.pyplot as plot
df=pd.read_csv('csv/HOBO_Master_40T_LR.csv')
a=df['slope'].values
print('a: ',a)  # a is an array with all the slopes

inversion=False
new_df=pd.DataFrame()
inv_count, inv_length=0, 0
i0, i_1, i_2, i_3 = 0, 0, 0, 0
new_df['invLen']=0

for i in range(0, len(a)):  # running through the entire data set
    i0=a[i]
    try:    # setting temporary variables as the data ahead of i
        i_1=a[i+1]
        i_2=a[i+2]
        i_3=a[i+3]
    except:
        i_1, i_2, i_3 = a[-1], a[-1], a[-1]

    if not inversion:   # if there is not an inversion, check for one
        if i0>0 and i_1>0 and i_2>0:
            inv_count+=1
            print('Inversion',inv_count,'started at:', df.iloc[i][0], df.iloc[i][1])
            new_df=new_df._append(df.iloc[[i]])
            new_df.at[i,['invLen']]=0
            inv_length += 1
            inversion=True
    elif inversion: # if there is an inversion, check to see if it will dissipate
        inv_length+=1
        if i_1<0 and i_2<0 and i_3<0:
            print('Inversion ended at: ', df.iloc[i+1][0], df.iloc[i+1][1], '\n')
            new_df=new_df._append(df.iloc[[i+1]])
            new_df.at[i+1,['invLen']]=inv_length
            inv_length = 0
            inversion = False

print('inversion count: ',inv_count)
new_df['Date']=pd.to_datetime(new_df['Date'])
new_df['Time']=new_df['Date'].dt.hour
new_df['Month']=new_df['Date'].dt.month
new_df.to_csv('csv/hours_with_inversion_master2.csv')    # a csv with all the hours with an inversion
print(new_df)

# # code to filter the inversion hours by month
# df=pd.read_csv('csv/hours_with_inversion_master.csv')
# df.drop(df.index[df['Month']!=12], inplace=True)
# df.to_csv('csv/December/dec_inversion_hours.csv')
# print(df)

# plotting the frequency of inversion starting and ending by month
# df=pd.read_csv('csv/May/may_inversion_hours.csv')
# df.drop(df.index[df['slope']>0], inplace=True)  # dropping slopes with a positive/negative lapse rate
# df1=pd.DataFrame()
# df1['Time']= df.Time.astype(pd.api.types.CategoricalDtype(categories=range(24)))
# df1 = (df1.Time.value_counts()/len(df))
# df1.sort_index(axis=0, ascending=True, inplace=True)
# df1.plot(x=1, y=2, figsize=(8,4), kind='bar')
# plot.title('Inversion End Times in May')
# plot.xlabel('Hour (EST)')
# plot.ylabel('Fraction of Inversions')
# plot.ylim([0,.38])
# n=str(len(df))
# inv_count_string='n='+n
# print(inv_count_string)
# plot.text(21,0.36, inv_count_string, fontsize=11)
# plot.show()


# bar graph of all inversions by length
# df=pd.read_csv('csv/hours_with_inversion_master2.csv')
# df.drop(df.index[df['invLen']==0], inplace=True)
# removing the warm season
# df.drop(df.index[df['Month']==5], inplace=True)
# df.drop(df.index[df['Month']==6], inplace=True)
# df.drop(df.index[df['Month']==7], inplace=True)
# df.drop(df.index[df['Month']==8], inplace=True)
# df.drop(df.index[df['Month']==9], inplace=True)
# df.drop(df.index[df['Month']==10], inplace=True)
# removing the cold season
# df.drop(df.index[df['Month']<5], inplace=True)
# df.drop(df.index[df['Month']>10], inplace=True)
# print(df)
# df1=pd.DataFrame()
# df1['invLen']= df.invLen.astype(pd.api.types.CategoricalDtype(categories=range(3,56)))
# df1 = (df1.invLen.value_counts()/len(df))
# df1.sort_index(axis=0, ascending=True, inplace=True)
# df1.plot(x=1, y=2, figsize=(8,5), kind='bar')
# plot.title("Inversion Lengths cold/warm season")
# plot.xlabel("length (hours)")
# plot.ylabel("fraction of inversions")
# plot.show()


# altering the dataframe to grab the data we want, =>6 hour inversions during the cold season

df=pd.read_csv('csv/hours_with_inversion_master2.csv')
df.drop(df.index[df['Month']==5], inplace=True)
df.drop(df.index[df['Month']==6], inplace=True)
df.drop(df.index[df['Month']==7], inplace=True)
df.drop(df.index[df['Month']==8], inplace=True)
df.drop(df.index[df['Month']==9], inplace=True)
df.drop(df.index[df['Month']==10], inplace=True)
# df.drop(df.index[df['invLen']<6], inplace=True)
df.to_csv('csv/cold_Season_invLen.csv')
print(df)
