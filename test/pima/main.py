import pandas as pd
import numpy as np
import sys

# Method 1: Load from a CSV file (if you have it downloaded)
# You can download from: https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database
df = pd.read_csv(sys.argv[1], delimiter=",")

# Or Method 2: Load from sklearn's datasets (if available)
# from sklearn.datasets import load_diabetes
# However, note that sklearn's load_diabetes() is a different dataset
# For Pima, you'll typically need the CSV file

# Get basic dataset information
print("Dataset Shape:")
print(df.shape)  # Shows (rows, columns)

print("\nColumn Names and Data Types:")
print(df.info())  # Shows column names, non-null counts, and data types

print("\nFirst few rows:")
print(df.head())  # Shows first 5 rows

print("\nLast few rows:")
print(df.tail())  # Shows last 5 rows

print("\nStatistical Summary:")
print(df.describe())  # Shows count, mean, std, min, quartiles, max

print("\nMissing Values:")
print(df.isnull().sum())  # Count of missing values per column

print("\nColumn Names:")
print(df.columns.tolist())

# print("\nValue Counts for Target Variable (Outcome):")
# print(df['Outcome'].value_counts())  # Distribution of target variable