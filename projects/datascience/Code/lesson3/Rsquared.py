import numpy as np

def compute_r_squared(data, predictions):
    # Write a function that, given two input numpy arrays, 'data', and 'predictions,'
    # returns the coefficient of determination, R^2, for the model that produced 
    # predictions.
    # 
    # Numpy has a couple of functions -- np.mean() and np.sum() --
    # that you might find useful, but you don't have to use them.

    # YOUR CODE GOES HERE
    '''
    sum1 = 0
    sum2 = 0
    #data_mean = np.mean(data)
    #print data_mean
   
    for i in range(v):
        sum1 += (data[i] - predictions[i])**2
        sum2 += (data[i] - data_mean)**2
    
    r_squared = 1 - sum1/sum2
    '''
    SST = ((data-np.mean(data))**2).sum()
    SSReg = ((predictions-data)**2).sum()
    r_squared = 1 - SSReg/SST
    
    return r_squared
