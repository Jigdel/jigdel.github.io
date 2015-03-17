import sys
import logging

from util import reducer_logfile
logging.basicConfig(filename=reducer_logfile, format='%(message)s',
                    level=logging.INFO, filemode='w')

def reducer():
    '''
    Given the output of the mapper for this assignment, the reducer should
    print one row per weather type, along with the average value of
    ENTRIESn_hourly for that weather type, separated by a tab. You can assume
    that the input to the reducer will be sorted by weather type, such that all
    entries corresponding to a given weather type will be grouped together.

    In order to compute the average value of ENTRIESn_hourly, you'll need to
    keep track of both the total riders per weather type and the number of
    hours with that weather type. That's why we've initialized the variable 
    riders and num_hours below. Feel free to use a different data structure in 
    your solution, though.

    An example output row might look like this:
    'fog-norain\t1105.32467557'

    Since you are printing the output of your program, printing a debug 
    statement will interfere with the operation of the grader. Instead, 
    use the logging module, which we've configured to log to a file printed 
    when you click "Test Run". For example:
    logging.info("My debugging message")
    '''

    total_riders = 0      # The number of total riders for this key
    num_hours = 0   # The number of hours with this key
    old_key = None

    for line in sys.stdin:
        data = line.strip().split("\t")
        
        if len(data) != 2:
            continue
        
        new_key, riders = data
        
        if old_key and old_key != new_key:
            # hourly average riders?
            #avg_riders = total_riders/num_hours
            print "{0}\t{1}".format(old_key,total_riders) #avg_riders)
            # assign them back to zero
            total_riders = 0
            num_hours = 0
        
        old_key = new_key
        # aggregate and increment riders and hours respectively
        total_riders += float(riders)
        #Not sure if this should be iterated here
        num_hours += 1
    
    #do not forget the last key
    if old_key != None:
        # Not sure if 'float(riders)' should be 'total_riders'
        #avg_riders = float(riders)/num_hours
        print "{0}\t{1}".format(old_key,total_riders)#avg_riders)

reducer()
