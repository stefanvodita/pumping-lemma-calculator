# K-Means Clustering
# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.cluster import KMeans

# Importing the dataset
dataset = pd.read_csv('data.csv', comment='#').iloc[:, [4, 5, 6]].values
print(dataset)
