import pandas as pd
df=pd.read_csv('Solar_Rad_Data1.csv')
# df['Date']=pd.to_datetime(df['Time'])
df.resample('60sec', on='Time').first()#.drop('datetime', 1).reset_index()


print(df)