import pandas as pd
from sklearn.model_selection import train_test_split
print("===================================================")
print("===================data selection==================")
print("===================================================")
data=pd.read_csv('Crop_recommendation.csv')
print(data.head(10))
print()
data_label=data['label']
print("===================================================")
print("=============checking missing values===============")
print("===================================================")
print(data.isna().sum())
print()
from sklearn import preprocessing