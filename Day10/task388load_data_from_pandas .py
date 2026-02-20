#Load a dataset using Pandas and explore it (e.g., Iris dataset). Example: pd.read_csv().
import pandas as pd
import os


#load iris dataset
script_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(script_dir, "iris.csv"))

# df.sample(5)     # random 5 rows

# print(df.info()) #print basic info

# print(df.describe()) #print descriptive statistics

# print(df.shape) #print shape


# print(df.columns) #print columns


# print(df.index) #print index


# print(df.values) #print values


# print(df.dtypes) #print dtypes


# print(df.head()) #first 5 rows


# print(df.tail()) #last 5 rows

#print(df.describe()) #print descriptive statistics (count,mean,std,min,max,25%,50%,75%)
#print(df.age.describe() )
print(df.isnull().sum()) #print number of missing values in each column
