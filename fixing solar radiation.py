import pandas as pd
df=pd.read_csv('csv/Solar_Rad_Data1.csv')
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df=(df.set_index('Datetime').apply(lambda x: x.asfreq('H')))
df=df.reset_index()
df.to_csv('Altered_Solar_Rad_data.csv')
print(df)