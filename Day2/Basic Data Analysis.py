""" You are provided with a dataset containing sales records for a retail store. Perform the
following tasks:
1. Load the dataset into a Pandas DataFrame and display the first 10 rows.
 """

import pandas as pd

df = pd.read_csv('d:/Piyush Domadiya/Day2/data.csv')
print(df.head(10))


#2. Clean the data by handling missing values and removing duplicates.
print("\nCleaning data...")
print(f"Original shape: {df.shape}")

# Remove duplicates
df = df.drop_duplicates()
print(f"After removing duplicates: {df.shape}")

# Handle missing values (drop rows with any missing values)
df = df.dropna()
print(f"After dropping missing values: {df.shape}")

print("Data cleaned.")


"""3. Calculate and display:
    o Total sales per product.
    o Total revenue per region.
    o The month with the highest sales. """
# Total sales per product
print("\nTotal sales per product:")
print(df.groupby('Product')['Total Revenue'].sum())

# Total revenue per region
print("\nTotal revenue per region:")
print(df.groupby('Region')['Total Revenue'].sum())

# The month with the highest sales
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
df['Month'] = df['Date'].apply(lambda x: x.strftime('%Y-%m'))
monthly_sales = df.groupby('Month')['Total Revenue'].sum()
highest_month = monthly_sales.idxmax()
print(f"\nThe month with the highest sales: {highest_month}")

""" 4. Visualize:
    o Sales trends over time using Matplotlib or Seaborn.
    o The top 5 products by revenue as a bar chart."""
import matplotlib.pyplot as plt
# Sales trends over time
sales_trends = df.groupby('Date')['Total Revenue'].sum().reset_index()
plt.plot(sales_trends['Date'], sales_trends['Total Revenue'])
plt.xlabel('Date')
plt.ylabel('Total Revenue')
plt.title('Sales Trends Over Time')
plt.show()

# Top 5 products by revenue
top_products = df.groupby('Product')['Total Revenue'].sum().nlargest(5).reset_index()
plt.bar(top_products['Product'], top_products['Total Revenue'])
plt.xlabel('Product')
plt.ylabel('Total Revenue')
plt.title('Top 5 Products by Revenue')
plt.show()