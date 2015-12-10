# Code from: 
# http://machinelearningmastery.com tutorials
# Using Python 2.7 - quick and dirty data analysis using Pandas.
# For more details see http://MachineLearningMastery.com

# Pima Indians diabetes dataset available at:
# https://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data


# Summarize Data

# load the data from CSV
import pandas as pd
names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
data = pd.read_csv('pima-indians-diabetes.data', names=names)

# view the data values
print(data)

# describe the data with summary statistics
print(data.describe())

# Visualize Data

# data distribution with box and whisker plots
import matplotlib.pyplot as plt
pd.options.display.mpl_style = 'default'
data.boxplot()

# review the data distribution with histograms
data.hist()

# compare feature distributions by class with histograms
data.groupby('class').hist()

# review the plas attribute distributions by class on the same plot
data.groupby('class').plas.hist(alpha=0.4)

# review relationships between attributes with pair-wise scatter plots
from pandas.tools.plotting import scatter_matrix
scatter_matrix(data, alpha=0.2, figsize=(6, 6), diagonal='kde')
