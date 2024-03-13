# -*- coding: utf-8 -*-
"""Automobile.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yBGtlfe5f6kLXtKX0TAdsltpQc3oC9iP
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import warnings

warnings.filterwarnings("ignore", "is_categorical_dtype")
warnings.filterwarnings("ignore", "use_inf_as_na")

# import dataset
df = pd.read_csv("Automobile_data.csv")

"""# Dataset Analysis"""

df.head()

df.shape

"""__Inferences__ :
* This dataset contains 205 rows and 26 features
"""

df.info()

"""__Inferences__ :
* This dataset contains :
    * 5 feature with float dtype
    * 5 feature with int dtype
    * 16 feature with object dtype
"""

df.isna().sum()

df.columns

"""__Inferences__:
* There are no missing or NaN values
"""

df.describe().T

# Analysis of unique values of objects
for col in df.select_dtypes('object'):
    print(f"{col} Unique Values:\n")
    print(df[col].unique())
    print("_" * 80)

"""__Inferences__:
* Within some features such as `peak-rpm`, `num-of-doors` , `normalized-losses` a question mark "?" is filled for some values

# Data Cleaning
"""

# Cleaning and removing "?" from "normalized-losses", "peak-rpm"
df[(df['peak-rpm'] == "?")]

df[(df['normalized-losses'] == '?')]

# "normalized_losses" feature
normalized_losses = df['normalized-losses'].loc[(df['normalized-losses'] != "?")]
normalized_losses_mean = normalized_losses.astype('int').mean()
df['normalized-losses'] = df['normalized-losses'].replace("?", normalized_losses_mean)

# "peak_rpm" feature
peak_rpm = df['peak-rpm'].loc[(df['peak-rpm'] != "?")]
peak_rpm_mean = peak_rpm.astype('int').mean()
df['peak-rpm'] = df['peak-rpm'].replace("?", peak_rpm_mean)

# num-of-doors feature
# for this feature , i would like to replace numbers as int with numbers as string
df['num-of-doors'] = df['num-of-doors'].replace("?", df['num-of-doors'].mode()[0])
door_mapping = {
    'two': 2,
    'three': 3,
    'four': 4
}
df['num-of-doors'] = df['num-of-doors'].map(door_mapping)

# Recheck "sum-of-doors"
df['num-of-doors'].unique()

# num-of-cylinders feature
# for this feature , i would like to replace numbers in str format with numbers with int
cylinders_mapping = {
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'tweleve': 12
}
df['num-of-cylinders'] = df['num-of-cylinders'].map(cylinders_mapping)

# Replacing "?" with rounded mean value
df.loc[(df['price'] == "?")]

prices = df['price'].loc[(df['price'] != "?")]
prices_mean = prices.astype("str").astype("int").mean()
df['price'] = df['price'].replace("?", prices_mean).astype("int")

# Replacing "?" with mean for "horsepower" feature
df[(df['horsepower'] == "?")]

hp = df['horsepower'].loc[(df['horsepower'] != "?")]
hp_mean = hp.astype('str').astype('int').mean()
df['horsepower'] = df['horsepower'].replace("?", hp_mean).astype("int")

# Replacing "?" with mean of "bore" feature
df[(df['bore'] == "?")]

bore = df['bore'].loc[(df['bore'] != "?")]
bore_mean = bore.astype('str').astype('float').mean()
df['bore'] = df['bore'].replace("?", bore_mean).astype("float")

# Replacing "?" with mean of "stroke" feature
df[(df['stroke'] == "?")]

stroke = df['stroke'].loc[(df['stroke'] != "?")]
stroke_mean = stroke.astype('str').astype('float').mean()
df['stroke'] = df['stroke'].replace("?", stroke_mean).astype('float')

# Creating a method to change the data types
def change_dtype(df, dtype, cols):
    for col in cols:
        df[col] = df[col].astype(dtype)

change_dtype(df, 'float', [["engine-size", "horsepower", "peak-rpm", "normalized-losses", "bore", "stroke"]])

# Check Dataframe
df.info()

# corret columns names
df.rename(columns={
        'normalized-losses': "normalized_losses",
        'fuel-type' : "fuel_type",
        'num-of-doors': "num_of_doors",
        'body-style' : "body_style",
        'drive-wheels': 'drive_wheels',
        'engine-location': 'engine_location',
        'wheel-base': 'wheel_base',
        'curb-weight': 'curb_weight',
        'engine-type': 'engine_type',
        'num-of-cylinders': 'num_of_cylinders',
        'engine-size': 'engine_size',
        'fuel-system': 'fuel_system',
        'compression-ratio': 'compression_ratio',
        'peak-rpm': 'peak_rpm',
        'city-mpg': 'city_mpg',
        'highway-mpg' : 'highway_mpg',

                }, inplace=True)

# check dataframe
df.head()

"""## Find and resolving outliers from numeric features"""

# Identify numeric columns
numeric_columns = df.select_dtypes(include=[np.number]).columns

# Visualize data using box plots
def plot_outliers(numeric_columns):
    for col in numeric_columns:
        plt.figure(figsize=(8, 4))
        sns.boxplot(x=col, data=df, color='skyblue', width=0.5)  # Adjust boxplot width and color
        plt.title(f'Boxplot of {col}', fontsize=16)  # Add title with appropriate font size
        plt.xlabel(f'{col}', fontsize=14)  # Add x-axis label with appropriate font size
        plt.grid(True, linestyle='--', alpha=0.7)  # Add grid lines with customized style and transparency
        plt.xticks(fontsize=12)  # Adjust x-axis tick font size
        plt.yticks(fontsize=12)  # Adjust y-axis tick font size
        plt.tight_layout()  # Adjust layout to prevent overlapping
        plt.show()
plot_outliers(numeric_columns)

# below funtion will find outliers by using IQR:
def detect_outliers_iqr(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    return (data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))

# creating a mask to find outliers
outliers = df[numeric_columns].apply(detect_outliers_iqr)

# lets check dataframe without outliers
df[~outliers.any(axis=1)].info()

"""* __Inferences__ :


When you have a limited dataset and removing outliers results in a significant loss of data, it's essential to consider alternative approaches to handle outliers without discarding too much information.
: Instead of removing outliers, you can impute them with a reasonable value. For numerical features, you can replace outliers with the median or mean of the respective feature. For categorical features, you can impute outliers with the mode.

## Impute Outliers with `median`
"""

# Apply the function to detect outliers
outliers_mask = detect_outliers_iqr(df.select_dtypes(include=['number']))

# Replace outliers with median
numeric_cols = df.select_dtypes(include=[np.number]).columns

# Imputation
for col in numeric_cols:
    median_val = df[col].median()  # Calculate median for each column
    df[col] = df[col].where(~outliers_mask[col], median_val)

# Lets check the boxplot of numeric features
plot_outliers(numeric_columns)

"""# EDA

### Barplot of categorical features
"""

def barplot(cols):
    for col in cols:
        plt.figure(figsize=(12, 6))
        sns.barplot(x=df[col].value_counts().index, y=df[col].value_counts(), data=df, palette='viridis')
        plt.title(f"{col}'s Barplot")
        plt.show()

categorical_features = df.select_dtypes('object').columns
barplot(categorical_features)

"""### Insurance risk ratings histogram"""

df.symboling.hist(bins=6,color='green');
plt.title("Insurance risk ratings of vehicles")
plt.ylabel('Number of vehicles')
plt.xlabel('Risk rating')
plt.show()

"""### Histogram of numeric features"""

def histogram(df, cols):
    for col in cols:
        plt.figure(figsize=(10, 5))
        sns.histplot(data=df, x=col, bins=50, kde=True, color='blue', edgecolor='black')
        plt.title(f"{col}'s Histogram", fontsize=12)
        plt.ylabel(f"{col}")
        plt.xlabel("Count")
        plt.show()

numeric_columns = df.select_dtypes(np.number).columns

histogram(df, numeric_columns)

"""### Correlation Heatmap"""

# Chossing numeric features
df_corr = df.corr(numeric_only=True)

# Plotting heatmatp
plt.figure(figsize=(12, 6))
sns.set_style('darkgrid')
sns.heatmap(data=df_corr, cmap='viridis', annot=True, fmt='.1f', linewidths=0.5)
plt.title('Heatmap Plot', fontsize=16)
plt.xlabel('X Axis', fontsize=12)
plt.ylabel('Y Axis', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
# Show the plot
plt.show()

"""# Scatter Plot of Engine Size Vs Horsepower"""

plt.figure(figsize=(12, 6))
sns.scatterplot(x='engine_size', y='horsepower', data=df, hue='fuel_type', palette='Set1')
plt.title("Scatter Plot of Engine Size Vs Horsepower")
plt.xlabel("Engine Size")
plt.ylabel("Horsepower")
plt.legend(title='Fuel Type')
plt.grid(True, linestyle="--", alpha=0.5)
plt.show()

"""# Boxplot of Make Vs Price"""

plt.figure(figsize=(16, 6))
sns.boxplot(x='make', y='price', data=df, hue='fuel_type')
plt.title('Box Plot of Price by Number of Doors')
plt.xlabel('Number of Doors')
plt.ylabel('Price')
plt.legend(title='Fuel Type')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

"""# Pair Plot of Numeric Features"""

sns.pairplot(df[['engine_size', 'horsepower', 'curb_weight', 'city_mpg', 'highway_mpg']])
plt.suptitle('Pair Plot of Selected Numeric Features', y=1.02)
plt.show()

"""# Count Plot of Fuel Type"""

plt.figure(figsize=(8, 6))
sns.countplot(x='fuel_type', data=df, palette='husl')
plt.title('Count Plot of Fuel Type')
plt.xlabel('Fuel Type')
plt.ylabel('Count')
plt.show()

"""# Facet Grid of Engine Size vs. Horsepower"""

g = sns.FacetGrid(df, col='fuel_type', hue='num_of_doors', height=4)
g.map(sns.scatterplot, 'engine_size', 'horsepower')
g.add_legend()
plt.subplots_adjust(top=0.85)
plt.suptitle('Facet Grid of Engine Size vs. Horsepower by Fuel Type and Number of Doors', fontsize=16)
plt.show()
