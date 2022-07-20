# FILTER NCEP/NCAR data for use in R package kohonen (self-organizing maps).
#  Normalizing of height data not recommended because more years of height data are needed
#   for a large enough climo dataset to normalize the heights.
# Also, plots ranked daily sum vs cumulative sum for identification of inflections
#  where large flux days account for a disproportionate amount of the cumulative sum

# from sklearn import preprocessing
import pandas as pd
import numpy as np
import netCDF4 as netcdf
from matplotlib import pyplot as plot
from datetime import date

#################### USER DEFINED VARIABLES ####################
### Define spatial domain of EOF analysis (in increments of 2.5 deg by 2.5 deg)
lat1 = 30
lat2 = 60  # domain for 2022 manuscript: 32.5-57.5, 275.0-300.0
lon1 = 272.5
lon2 = 302.5
### Months to include (must be contiguous); inclusive
mon1 = 6
mon2 = 9
### Hours of day to include (must be contiguous), not cross midnight; inclusive
hr1 = 6
hr2 = 18
### Filter heights by variable threshold? Which variable and threshold?
filter_by_var = "PET"  # best_FC or best_LE or none (to not filter by variable threshold)
threshold = 0  # LE = 4626 and 2790;  FC = -335 and -276; check >< sign on lines ~142 or 154; PET = 9460 and 6620
### Output csv file name
filename = "hgt_data_PET_20220622.csv"  # output filename of height data for SOM analysis
filename2 = "member_dates_PET.csv"  # output filename for dates that meet the threshold criteria; in chronological order
################################################################

### Open remote reanalysis dataset; coding follows Numpy convention (not pandas dataframes)
fin0 = netcdf.Dataset('height files/hgt.2013.nc', 'r')
fin1 = netcdf.Dataset('height files/hgt.2014.nc', 'r')
fin2 = netcdf.Dataset('height files/hgt.2015.nc', 'r')
fin3 = netcdf.Dataset('height files/hgt.2016.nc', 'r')
fin4 = netcdf.Dataset('height files/hgt.2017.nc', 'r')
fin5 = netcdf.Dataset('height files/hgt.2018.nc', 'r')
fin6 = netcdf.Dataset('height files/hgt.2019.nc', 'r')
fin1.variables.keys()
levels = fin1.variables['level'][:]
lats = fin1.variables['lat'][:]
lons = fin1.variables['lon'][:]
time0 = fin0.variables['time'][:]
time1 = fin1.variables['time'][:]
time2 = fin2.variables['time'][:]
time3 = fin3.variables['time'][:]
time4 = fin4.variables['time'][:]
time5 = fin5.variables['time'][:]
time6 = fin6.variables['time'][:]
base = date(1800, 1, 1)  # reference date/time for netcdf file time variable
timevar0 = pd.to_timedelta(time0, unit='h') + pd.Timestamp(base)
timevar1 = pd.to_timedelta(time1, unit='h') + pd.Timestamp(base)
timevar2 = pd.to_timedelta(time2, unit='h') + pd.Timestamp(base)
timevar3 = pd.to_timedelta(time3, unit='h') + pd.Timestamp(base)
timevar4 = pd.to_timedelta(time4, unit='h') + pd.Timestamp(base)
timevar5 = pd.to_timedelta(time5, unit='h') + pd.Timestamp(base)
timevar6 = pd.to_timedelta(time6, unit='h') + pd.Timestamp(base)
timevar0 = pd.DataFrame(timevar0, columns=['datetime'])
timevar1 = pd.DataFrame(timevar1, columns=['datetime'])
timevar2 = pd.DataFrame(timevar2, columns=['datetime'])
timevar3 = pd.DataFrame(timevar3, columns=['datetime'])
timevar4 = pd.DataFrame(timevar4, columns=['datetime'])
timevar5 = pd.DataFrame(timevar5, columns=['datetime'])
timevar6 = pd.DataFrame(timevar6, columns=['datetime'])
lat_bnds, lon_bnds = [lat1, lat2], [lon1, lon2]
# lat_bnds, lon_bnds = [39, 51], [282, 294]
concat_NCEPdata = pd.DataFrame()
k = 0
for i in [850]:
    level_ind = np.where((levels == i))  # choose pressure level
    lat_inds = np.where((lats >= lat_bnds[0]) & (lats <= lat_bnds[1]))[0]
    lon_inds = np.where((lons >= lon_bnds[0]) & (lons <= lon_bnds[1]))[0]
    hgt_subset0 = fin0.variables['hgt'][:, np.ndarray.item(level_ind[0]), lat_inds[:], lon_inds[:]]
    hgt_subset1 = fin1.variables['hgt'][:, np.ndarray.item(level_ind[0]), lat_inds[:], lon_inds[:]]
    hgt_subset2 = fin2.variables['hgt'][:, np.ndarray.item(level_ind[0]), lat_inds[:], lon_inds[:]]
    hgt_subset3 = fin3.variables['hgt'][:, np.ndarray.item(level_ind[0]), lat_inds[:], lon_inds[:]]
    hgt_subset4 = fin4.variables['hgt'][:, np.ndarray.item(level_ind[0]), lat_inds[:], lon_inds[:]]
    hgt_subset5 = fin5.variables['hgt'][:, np.ndarray.item(level_ind[0]), lat_inds[:], lon_inds[:]]
    hgt_subset6 = fin6.variables['hgt'][:, np.ndarray.item(level_ind[0]), lat_inds[:], lon_inds[:]]
    hgt_subset0 = hgt_subset0.data
    hgt_subset1 = hgt_subset1.data
    hgt_subset2 = hgt_subset2.data
    hgt_subset3 = hgt_subset3.data
    hgt_subset4 = hgt_subset4.data
    hgt_subset5 = hgt_subset5.data
    hgt_subset6 = hgt_subset6.data
    t = hgt_subset1.shape[0]
    x = hgt_subset1.shape[1]
    y = hgt_subset1.shape[2]
    # print(t,x,y)
    # print(hgt_subset0[130][10][6])
    hgt_subset2d0 = np.reshape(hgt_subset0, (t, x*y))  # Reshape array to 2D: Rows=date, Columns=gridpoint
    hgt_subset2d1 = np.reshape(hgt_subset1, (t, x*y))  #
    hgt_subset2d2 = np.reshape(hgt_subset2, (t, x*y))  #
    hgt_subset2d3 = np.reshape(hgt_subset3, (t+4, x*y))  #
    hgt_subset2d4 = np.reshape(hgt_subset4, (t, x*y))  # t+1 is for leap years
    hgt_subset2d5 = np.reshape(hgt_subset5, (t, x*y))  #
    hgt_subset2d6 = np.reshape(hgt_subset6, (t, x*y))  #

    hgt_subset2d0 = pd.DataFrame(hgt_subset2d0)  # convert numpy array to dataframe for concatonation with datetime var 'timevar'
    hgt_subset2d1 = pd.DataFrame(hgt_subset2d1)  #
    hgt_subset2d2 = pd.DataFrame(hgt_subset2d2)  #
    hgt_subset2d3 = pd.DataFrame(hgt_subset2d3)  #
    hgt_subset2d4 = pd.DataFrame(hgt_subset2d4)  #
    hgt_subset2d5 = pd.DataFrame(hgt_subset2d5)  #
    hgt_subset2d6 = pd.DataFrame(hgt_subset2d6)  #

    hgt_subset2Dt0 = pd.concat([timevar0, hgt_subset2d0], axis=1)  # concatonate time variable and gridpoint dataframes
    hgt_subset2Dt1 = pd.concat([timevar1, hgt_subset2d1], axis=1)  #
    hgt_subset2Dt2 = pd.concat([timevar2, hgt_subset2d2], axis=1)  #
    hgt_subset2Dt3 = pd.concat([timevar3, hgt_subset2d3], axis=1)  #
    hgt_subset2Dt4 = pd.concat([timevar4, hgt_subset2d4], axis=1)  #
    hgt_subset2Dt5 = pd.concat([timevar5, hgt_subset2d5], axis=1)  #
    hgt_subset2Dt6 = pd.concat([timevar6, hgt_subset2d6], axis=1)  #

    hgt_subset2Dt0 = hgt_subset2Dt0.set_index(pd.DatetimeIndex(hgt_subset2Dt0['datetime']))  # set index to be datetime format
    hgt_subset2Dt1 = hgt_subset2Dt1.set_index(pd.DatetimeIndex(hgt_subset2Dt1['datetime']))  #
    hgt_subset2Dt2 = hgt_subset2Dt2.set_index(pd.DatetimeIndex(hgt_subset2Dt2['datetime']))  #
    hgt_subset2Dt3 = hgt_subset2Dt3.set_index(pd.DatetimeIndex(hgt_subset2Dt3['datetime']))  #
    hgt_subset2Dt4 = hgt_subset2Dt4.set_index(pd.DatetimeIndex(hgt_subset2Dt4['datetime']))  #
    hgt_subset2Dt5 = hgt_subset2Dt5.set_index(pd.DatetimeIndex(hgt_subset2Dt5['datetime']))  #
    hgt_subset2Dt6 = hgt_subset2Dt6.set_index(pd.DatetimeIndex(hgt_subset2Dt6['datetime']))  #

    if k == 0:
        concat_NCEPdata = pd.concat(
            [hgt_subset2Dt0, hgt_subset2Dt1, hgt_subset2Dt2, hgt_subset2Dt3, hgt_subset2Dt4, hgt_subset2Dt5, hgt_subset2Dt6],
            axis=0)  # Concatonate all years of NCEP-NCAR reanalysis data
    elif k >= 1:
        subset_all = pd.concat(
            [hgt_subset2Dt0, hgt_subset2Dt1, hgt_subset2Dt2, hgt_subset2Dt3, hgt_subset2Dt4, hgt_subset2Dt5, hgt_subset2Dt6],
            axis=0)  # concatontate each additional pressure level of heights
        concat_NCEPdata = pd.concat([concat_NCEPdata, subset_all], axis=1)
    k = k + 1


concat_NCEPdata = concat_NCEPdata.drop(['datetime'], axis=1)  # drop the redundant datetime column
# rename columns to eliminate repeated column names
noclmns = len(lat_inds) * len(lon_inds)
concat_NCEPdata.columns = range(noclmns)
#  Calculate gridpoint deviations (to remove seasonality of geopotential height values)
### Calculate centered 13-day average for each day for each gridpoint
smooth_NCEPdata = pd.DataFrame()
for i in concat_NCEPdata[:]:
    smooth_NCEPdata[i] = concat_NCEPdata.iloc[:, i].rolling(window=13, center=True).mean()
### Calculate deviations of daily data from the 13-day running average
dev_NCEPdata = concat_NCEPdata - smooth_NCEPdata
dev_NCEPdata = dev_NCEPdata.loc[(dev_NCEPdata.index.month <= 4) | (dev_NCEPdata.index.month >= 11)] # isolate cold season
dev_NCEPdata = dev_NCEPdata.loc['11/5/2013 05:00':'11/6/2019 21:00']  # isolate growing season
dev_NCEPdata = dev_NCEPdata.reset_index()

# print(dev_NCEPdata)

inv_start=pd.read_csv('csv/cold_Season_invLen_start times only.csv')
inv_start=inv_start.rename({'Date':'datetime'}, axis=1)
inv_start['datetime'] = pd.to_datetime(inv_start['datetime'])
inv_start['inv_time'] = inv_start['datetime'].dt.time
inv_start['inv_date'] = inv_start['datetime'].dt.date
dev_NCEPdata['datetime'] = pd.to_datetime(dev_NCEPdata['datetime'])
dev_NCEPdata['hgt_time'] = dev_NCEPdata['datetime'].dt.time
dev_NCEPdata['hgt_date'] = dev_NCEPdata['datetime'].dt.date
# Sort the two dataframes by the new key, as required by merge_asof function
inv_start.sort_values(by="datetime", inplace=True, ignore_index=True)
dev_NCEPdata.sort_values(by="datetime", inplace=True, ignore_index=True)
result_df=pd.merge_asof(inv_start, dev_NCEPdata, on="datetime", direction="nearest")
# make a final NCEP csv that has datetime (from height data at time closest to inv end times) and dev_NCEP data

final_NCEPdata=pd.DataFrame()
final_NCEPdata=result_df
final_NCEPdata['Datetime']=result_df['hgt_date'].astype(str)+' '+result_df['hgt_time'].astype(str)
final_NCEPdata=final_NCEPdata.drop(final_NCEPdata.columns[[0,1,2,3,173,174]], axis=1)
final_NCEPdata=final_NCEPdata.set_index(final_NCEPdata['Datetime'])     # set datetime column as index
final_NCEPdata=final_NCEPdata.drop(['Datetime'], axis=1)
# final_NCEPdata.to_csv('csv/NCEPdata.csv')
print(final_NCEPdata)

average_array=final_NCEPdata.mean()
print("asd", max(average_array), min(average_array))
average_array=average_array.to_numpy()
average_array=average_array.reshape([13,13])
print(average_array)
aa_df=pd.DataFrame(average_array)
print(aa_df)
aa_df.to_csv('csv/class_.csv')
































# # normalizeyn = input("Do you want to normalize the gridpoint residuals? (yes/no):\n")
# # if normalizeyn == "yes":
# #     # Normalize the gridded data along each column individually
# #     norm_NCEPdata = preprocessing.normalize(dev_NCEPdata, axis=0)*10 # normalized data comes out very small (-0.04 to 0.04), so multiplied by 10
# #     norm_NCEPdata = pd.DataFrame(norm_NCEPdata)
# #     final_NCEPdata = norm_NCEPdata.set_index(dev_NCEPdata.index)
# # elif normalizeyn == "no":
# #     final_NCEPdata = dev_NCEPdata
# #     print("normalizing not performed")
#
# final_NCEPdata = dev_NCEPdata  # REMOVE THIS LINE WHEN UNCOMMENTING ABOVE NORMALIZATION OPTION
#
# ###### Read in flux tower data ######
# fin_flux = pd.read_csv('/Users/ekelsey2/Documents/Research/coding/HBEF/HBR_flux_gap_filled_20220622.csv')
# flux = fin_flux.loc[:, ('time', 'best_LE', 'best_FC', 'PET')]
# flux['datetime'] = flux['time']
# flux = flux.set_index('datetime')
# flux.drop(['time'], axis=1, inplace=True)
# flux.index = pd.to_datetime(flux.index)
# ###### Filter by flux variable ######
# if filter_by_var == "best_FC":
#     flux_var = flux['best_FC']  # Set flux tower variable to use in analysis
#     flux_var = flux_var.dropna()  # get rid of any NaN
#     flux_hourly = flux_var.loc[(flux_var.index.hour >= hr1) & (flux_var.index.hour <= hr2)]
#     flux_daily = flux_hourly.groupby(flux_hourly.index.date).sum()
#     flux_daily = (flux_daily / 26) * 13 * 60 * 60
#     # Extract all days when FC exceeded a threshold
#     flux_daily = pd.DataFrame(flux_daily)  # make flux_daily a DataFrame for .loc function to work (on next line)
#     # Isolate months of choice - next two lines needed for daily_sum_plot option below
#     flux_daily.index = pd.to_datetime(flux_daily.index)
#     flux_daily = flux_daily.loc[(flux_daily.index.month >= mon1) & (flux_daily.index.month <= mon2)]
#     # thresh_dates used after plotting for to create filtered height file for SOM analysis
#     thresh_dates = flux_daily.loc[flux_daily[
#                                       filter_by_var] < threshold]  # !#! get days in monthly window that ET meets criteria !ENSURE SIGN IS CORRECT
# elif filter_by_var == "best_LE" or "PET":
#     flux_var = flux[filter_by_var]  # Set flux tower variable to use in analysis
#     flux_var = flux_var.dropna()  # get rid of any NaN
#     flux_hourly = flux_var.loc[(flux_var.index.hour >= hr1) & (flux_var.index.hour <= hr2)]
#     flux_daily = flux_hourly.groupby(flux_hourly.index.date).sum()
#     flux_daily.index = pd.to_datetime(flux_daily.index)  # set index to be datetime format
#     # Extract all days when ET exceeds a threshold
#     flux_daily = pd.DataFrame(flux_daily)  # make flux_daily a DataFrame for .loc function to work (on next line)
#     # Isolate months of choice - next two lines needed for daily_sum_plot option below
#     flux_daily.index = pd.to_datetime(flux_daily.index)
#     flux_daily = flux_daily.loc[(flux_daily.index.month >= mon1) & (flux_daily.index.month <= mon2)]
#     # thresh_dates used after plotting for to create filtered height file for SOM analysis
#     thresh_dates = flux_daily.loc[flux_daily[
#                                       filter_by_var] > threshold]  # !#! get days in monthly window that ET meets criteria !ENSURE SIGN IS CORRECT
#
# elif filter_by_var == "none":
#     print("no filtering by flux variable chosen")
# # flux_daily.to_csv("ETflux_daily.csv", index=True, header=True)
# # filt_dates.to_csv("ETfilt_dates.csv", index=True, header=True)
#
# daily_sum_plot = input("Do you want to plot daily sum versus cumulative sum and percent? (yes/no):\n")
# if daily_sum_plot == "yes":
#     ### Calculate and plot ranked daily sums vs cumulative daily sum - to determine LE&FC thresholds for SOM analysis
#     flux_hourly = flux_hourly.loc[
#         (flux_hourly.index.month >= mon1) & (flux_hourly.index.month <= mon2)]  # filter months
#     flux_hourly.index = pd.to_datetime(
#         flux_hourly.index)  # giv variable the correct type for the next line to work ( groupby().count() )
#     y = flux_hourly.groupby(flux_hourly.index.date).count()  # count how many data points per day
#     y = pd.DataFrame(y)  # make y a DataFrame so the next two lines will work
#     y['count'] = y[filter_by_var]  # create new count variable with a good column name
#     y.drop([filter_by_var], axis=1, inplace=True)  # remove old count variable with the wrong name
#     y = pd.concat([y, flux_daily[filter_by_var]], axis=1)  # add column of daytime sum of variable
#     y_sorted = y[(y['count'] == 26)]  # filter to retain only days with full data
#     y_sorted = y_sorted.sort_values(by=[filter_by_var])
#     y_sorted['CUMSUM'] = y_sorted[filter_by_var].cumsum()  # add column of the cumulative sum of the variable
#     cum_sum = y_sorted['CUMSUM'].max()  ###!!! SWITCH TO MIN FOR FC, MAX FOR ET AND PET  !!!###
#     y_sorted['percent'] = y_sorted['CUMSUM'] / cum_sum
#
#     if filter_by_var == "best_FC":
#         print("BEST FC")
#         # AVERAGE FC THEN MULITPLY by 13hr*60min*60sec
#
#         plt.figure(1)
#         plt.plot(y_sorted[filter_by_var], y_sorted['CUMSUM'])
#         plt.xlabel("umol C/m2")
#         plt.figure(2)
#         plt.plot(y_sorted[filter_by_var], y_sorted['percent'])
#         plt.xlabel("umol C/m2")
#         plt.ylabel("fraction of total FC")
#         plt.figure(3)
#         dailyflux = pd.Series(y_sorted[filter_by_var])
#         dailyflux.plot.hist(grid=True, bins=20, rwidth=0.9)
#         plt.xlabel("umol C/m2")
#         plt.grid(axis='x')
#         plt.show()
#
#     elif filter_by_var == "best_ET" or "PET":  # !!! DON'T MUTIPLY BY .000734 for PET!!!
#         print("ET or PET")
#         plt.figure(1)
#         plt.plot(y_sorted[filter_by_var], y_sorted['CUMSUM'])  # *.000734
#         plt.xlabel("mm of water")
#         plt.figure(2)
#         plt.plot(y_sorted[filter_by_var], y_sorted['percent'])  # *.000734
#         plt.xlabel("mm of water")
#         plt.ylabel("fraction of total PET")  # CHANGE VAR
#         plt.figure(3)
#         dailyflux = pd.Series(y_sorted[filter_by_var])  # *.000734
#         dailyflux.plot.hist(grid=True, bins=20, rwidth=0.9)
#         plt.xlabel("mm of water")
#         plt.ylabel("number of days")
#         plt.grid(axis='x')
#         plt.show()
#     elif daily_sum_plot == "no":
#         print("end of script")
#
#     ### GET SUBSET OF DAYS OF HEIGHT DATA BY FLUX VARIABLE THRESHOLD
# if filter_by_var != "none":
#     ### thresh_dates has all days filtered by threshold; now filter this to keep only days of complete data, which y-sorted['count'] has
#     thresh_dates = thresh_dates[thresh_dates.index.isin(y_sorted.index)]
#     subset_hgts = final_NCEPdata[
#         final_NCEPdata.index.isin(thresh_dates.index)]  # get heights for days that ET meets criteria
#     subset_hgts.index = pd.to_datetime(subset_hgts.index)
#     subset_hgts.to_csv(filename, index=True,
#                        header=True)  # save height data to csv to analysis in Kohonen SOM package in R
#     thresh_dates.to_csv(filename2, index=True, header=True)
# elif filter_by_var == "none":
#     final_NCEPdata.to_csv(filename, index=True, header=True)  # save height data to csv to analysis
