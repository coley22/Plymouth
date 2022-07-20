### Plots the residual height composites for each SOM class.
#   Number of SOM classes to plot is specified by i in for loop
### Secondarily, SOM statistics to help determine the best number of classes to use is calculated.
### Third, statistics are produced for each cluster: meanT, meanNETRAD, meanVPD

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

lat1 = 32.5; lat2 = 57.5
lon1 = 275; lon2 = 300
### Months to include (must be contiguous); inclusive
mon1 = 6; mon2 = 9
### Hours of day to include (must be contiguous), not cross midnight; inclusive
hr1 = 6; hr2 = 18

m=1 # number of classes
n = range(1,m+1,1) ### !!! ### change middle number to the number of classes +1

for i in n:
    fin = pd.read_csv('csv/class_.csv'+str(i)+'.csv', header=None)
    D_sum = 0 # reset variable
    lats = np.arange(lat1,lat2+.1,2.5) # upper bound (second number) must be slightly higher than last number needed for inclusion
    lons = np.arange(lon1,lon2+.1,2.5)
    plt.figure(i, figsize=(11,14))
    mapcrs = ccrs.LambertConformal(central_longitude=-71, central_latitude=44, standard_parallels=(30, 60))
    ax = plt.subplot(111,projection=mapcrs)
    # Set up the projection of the data; if lat/lon then PlateCarree is what you want
    datacrs = ccrs.PlateCarree()
    ax.set_extent([-85,-59,31,58], ccrs.PlateCarree())  # original extent: -82,-62,36,53
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
    ax.add_feature(cfeature.STATES.with_scale('50m'))
    clevs = np.linspace(-1.0, 1.0, 21)  # contour values of variable being plotted
    cf = ax.contourf(lons,lats, fin, clevs, cmap=plt.cm.bwr, transform=datacrs)
    cb = plt.colorbar(cf,orientation='horizontal',pad=0,aspect=50)
    cb.ax.tick_params(labelsize=20)
    cb.set_label(label='850 hPa geopotential height residuals (m)', size=20)
    csf = ax.contour(lons, lats, fin, clevs, colors='grey',linestyles='solid', transform=datacrs)
    plt.clabel(csf, fmt='%d',fontsize=0)
    # Use units of mol/m2 for FC, mm for et and PET:   Mean C-flux = {:.0f}'.format(var_integer)+' mmol/m2' or
    plt.title('Composite')

plt.show()