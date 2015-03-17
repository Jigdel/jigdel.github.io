from pandas import *
from ggplot import *

def plot_weather_data(turnstile_weather):
    ''' 
    plot_weather_data is passed a dataframe called turnstile_weather. 
    Use turnstile_weather along with ggplot to make another data visualization
    focused on the MTA and weather data we used in Project 3.
    
    Make a type of visualization different than what you did in the previous exercise.
    Try to use the data in a different way (e.g., if you made a lineplot concerning 
    ridership and time of day in exercise #1, maybe look at weather and try to make a 
    histogram in this exercise). Or try to use multiple encodings in your graph if 
    you didn't in the previous exercise.
    
    You should feel free to implement something that we discussed in class 
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time-of-day or day-of-week
     * How ridership varies by subway station
     * Which stations have more exits or entries at different times of day

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/
     
    You can check out the link 
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    to see all the columns and data points included in the turnstile_weather 
    dataframe.
     
   However, due to the limitation of our Amazon EC2 server, we are giving you a random
    subset, about 1/3 of the actual data in the turnstile_weather dataframe.
    '''

    # Scatter Plot - Hourly entry traffic based on stations
    #b + geom_boxplot(aes(fill = X1), stat = "identity")
    # Source: http://docs.ggplot2.org/current/geom_boxplot.html

    # http://jeromyanglim.blogspot.ca/2012/05/how-to-plot-three-categorical-variables.html
    # I would like to further explore different three categories (rain/fog/etc.) and plot them for the blog
    # http://stackoverflow.com/questions/22717680/ggplot2-change-color-of-line-based-on-categorical-variable
    
    '''
    p = ggplot(turnstile_weather, aes('UNIT', 'ENTRIESn_hourly'))#, fill = 'UNIT'))
    limit_axes = xlim(-.75, 24.5) + ylim(0, 48000)
    plot = p + geom_boxplot() + labs('Stations', 'Entries') #+ limit_axes
    '''
    '''
    # Histogram - Hourly EXIT traffic
    p = ggplot(turnstile_weather, aes('EXITSn_hourly'))
    limit_axes = xlim(0, 15000)
    plot = p + geom_histogram() + limit_axes + ggtitle('Histogram of hourly exits') + labs('Exits', 'Freq')
    '''
    p = ggplot(turnstile_weather, aes('Hour', 'ENTRIESn_hourly'))
    plot = p + geom_point(color = 'red') + geom_line(color = 'red')
    #plot = # your code here
    
    return plot
