from pandas import *
from ggplot import *

def plot_weather_data(turnstile_weather):
    '''
    You are passed in a dataframe called turnstile_weather. 
    Use turnstile_weather along with ggplot to make a data visualization
    focused on the MTA and weather data we used in assignment #3.  
    You should feel free to implement something that we discussed in class 
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.  

   
    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/
     
    You can check out:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
     
    To see all the columns and data points included in the turnstile_weather 
    dataframe. 
    
    However, due to the limitation of our Amazon EC2 server, we are giving you a random
    subset, about 1/3 of the actual data in the turnstile_weather dataframe.
    
    #headers
    UNIT
    DATEn
    TIMEn
    Hour
    DESCn
    ENTRIESn_hourly
    EXITSn_hourly
    maxpressurei
    maxdewpti
    mindewpti
    minpressurei
    meandewpti
    meanpressurei
    fog
    rain
    meanwindspdi
    mintempi
    meantempi
    maxtempi
    precipi
    thunder
    
    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time of day or day of week
     * How ridership varies based on Subway station
     * Which stations have more exits or entries at different times of day
    '''
    
    # your code here 
    #plot graph
    #plot = ggplot(turnstile_weather, aes('Hour', 'EXITSn_hourly')) + geom_point(color='red') + geom_line(color='blue') + xlab('Hour') + ylab('EXITSn_hourly') + ggtitle('Title to be decided')
    #some_data = pandas.melt(turnstile_weather, id_vars=['DATEn'])
    
    '''
    # Histogram - Hourly EXIT traffic
    p = ggplot(turnstile_weather, aes('EXITSn_hourly'))
    limit_axes = xlim(0, 15000)
    plot = p + geom_histogram() + limit_axes + ggtitle('Histogram of hourly exits') + labs('Exits', 'Freq')
    '''
    
    '''
    # Histogram - Hourly ENTRY traffic
    p = ggplot(turnstile_weather, aes('ENTRIESn_hourly'))
    #limit_axes = scale_x_continuous(limits = c(0, 15000))
    limit_axes = xlim(0, 15000)
    plot = p + geom_histogram() + limit_axes + ggtitle('Histogram of hourly entries') + labs('Entries', 'Freq')
    '''
    
    '''
    # Hourly entry traffic
    p = ggplot(turnstile_weather, aes('Hour', 'ENTRIESn_hourly'))
    plot = p + geom_point(color = 'red') + geom_line(color = 'red')
    '''
    # Density
    p = ggplot(turnstile_weather, aes('ENTRIESn_hourly', color = 'rain')) #precipi
    limit_axes_labels = xlim(0, 15000) #+ labs('Entries', 'Precipitation')
    plot = p + geom_density() + limit_axes_labels #+ ggtitle('Histogram of hourly exits') 
    #plot = p + geom_point(color = 'red') + geom_line(color = 'red')
    
    #plot = p + geom_point() + stat_smooth(color='red')
    #plot = ggplot(
    return plot
