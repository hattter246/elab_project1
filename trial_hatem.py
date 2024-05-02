import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
pd.set_option('display.max_columns', None)

# Define department code to department name mapping
department_mapping = {
    1: "Bakery & Pastry",
    2: "Beer & Wine",
    3: "Books & Magazines",
    4: "Candy & Chips",
    5: "Care & Hygiene",
    6: "Cereals & Spreads",
    7: "Cheese & Tapas",
    8: "Dairy & Eggs",
    9: "Freezer",
    10: "Fruit & Vegetables",
    11: "Household & Pet",
    12: "Meat & Fish",
    13: "Pasta & Rice",
    14: "Salads & Meals",
    15: "Sauces & Spices",
    16: "Soda & Juices",
    17: "Special Diet",
    18: "Vegetarian & Vegan"
}

# Open the CSV file and parse each line manually
parsed_data = []
customer_id = 0  # Initialize customer_id
with open("supermarket_fixed2.csv", "r") as file:
    for line in file:
        transactions = line.strip().split(", ")
        for transaction in transactions:
            parts = transaction.split()
            if len(parts) == 3:
                department_code, time_elapsed, price = parts
                price = price.replace(',', '')  # Remove all commas from price string
                department = department_mapping.get(int(department_code), "Unknown Department")
                try:
                    time_elapsed = int(time_elapsed)
                    price = float(price)
                    parsed_data.append({
                        "customer_id": customer_id,  # Include customer_id
                        "department": department,
                        "time_elapsed": time_elapsed,
                        "price": price
                    })
                except ValueError:
                    print("Error converting data:", parts)
        customer_id += 1  # Increment customer_id for each line
# Create a DataFrame from the parsed data
df = pd.DataFrame(parsed_data)
print(df.head())

# EDA: Boxplots and Histograms
features = ['time_elapsed', 'price']
plt.figure(figsize=(12, 6))
for i, feature in enumerate(features, 1):
    plt.subplot(1, 2, i)
    sns.boxplot(y=df[feature])
    plt.title(f'Boxplot of {feature}')

plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
for i, feature in enumerate(features, 1):
    plt.subplot(1, 2, i)
    sns.histplot(df[feature], bins=30, kde=True)
    plt.title(f'Distribution of {feature}')

plt.tight_layout()
plt.show()

# Frequency plot for department visits
department_counts = df['department'].value_counts()
plt.figure(figsize=(12, 6))
sns.barplot(x=department_counts.index, y=department_counts.values, palette='viridis')
plt.title('Frequency of Department Visits')
plt.xlabel('Department')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.show()

# Grouping data by customer_id
customer_stats = df.groupby('customer_id').agg(
    total_spent=pd.NamedAgg(column='price', aggfunc='sum'),
    total_items=pd.NamedAgg(column='price', aggfunc='size'),
    avg_spent_per_visit=pd.NamedAgg(column='price', aggfunc='mean'),
    total_time=pd.NamedAgg(column='time_elapsed', aggfunc='sum')
).reset_index()

print(customer_stats.head())

# Visualizing total spending per customer
plt.figure(figsize=(12, 6))
sns.histplot(customer_stats['total_spent'], bins=30, kde=True)
plt.title('Distribution of Total Spending per Customer')
plt.xlabel('Total Spent')
plt.ylabel('Number of Customers')
plt.show()


# Feature engineering
customer_totals = df.groupby('customer_id').agg(total_spent=pd.NamedAgg(column='price', aggfunc='sum'))
# Average purchase value, maximum, minimum purchase per visit
customer_averages = df.groupby('customer_id').agg(avg_spent=pd.NamedAgg(column='price', aggfunc='mean'),
                                                  max_spent=pd.NamedAgg(column='price', aggfunc='max'),
                                                  min_spent=pd.NamedAgg(column='price', aggfunc='min'))

# Visit duration
visit_duration = df.groupby('customer_id')['time_elapsed'].transform('sum')

# Department visit counts
department_counts = pd.get_dummies(df['department']).groupby(df['customer_id']).sum()
# Avg time between scans
avg_time_between_scans = df.groupby('customer_id')['time_elapsed'].transform(lambda x: x.mean())
# Combine features into a single DataFrame
features_df = pd.concat([customer_totals, customer_averages, department_counts, visit_duration, avg_time_between_scans],
                        axis=1)
print(features_df.head())

# Assuming we have already calculated customer_stats dataframe and features_df dataframe

# Frequency of Visits
customer_stats['visit_frequency'] = pd.qcut(customer_stats['total_items'], q=4,
                                             labels=['Low', 'Medium-Low', 'Medium-High', 'High'])

# Total Spending
customer_stats['spending_category'] = pd.qcut(customer_stats['total_spent'], q=4,
                                               labels=['Low', 'Medium-Low', 'Medium-High', 'High'])

# Average Spending per Visit
customer_stats['avg_spending_per_visit'] = pd.qcut(customer_stats['avg_spent_per_visit'], q=4,
                                                    labels=['Low', 'Medium-Low', 'Medium-High', 'High'])

# Time Spent in Store
customer_stats['time_spent_category'] = pd.qcut(customer_stats['total_time'], q=4,
                                                 labels=['Low', 'Medium-Low', 'Medium-High', 'High'])


# Now, let's combine these customer profiling features with other features in features_df
features_df = pd.concat([features_df, customer_stats[['visit_frequency', 'spending_category',
                                                      'avg_spending_per_visit', 'time_spent_category']]], axis=1)

print(features_df.head())

# Create subplots for overlaid histograms
plt.figure(figsize=(12, 6))

# Histogram for Total Spending
plt.subplot(1, 2, 1)
for category in customer_stats['spending_category'].unique():
    sns.histplot(customer_stats[customer_stats['spending_category'] == category]['total_spent'], bins=30,
                 kde=True, label=category, alpha=0.5)
plt.title('Distribution of Total Spending by Spending Category')
plt.xlabel('Total Spending')
plt.ylabel('Frequency')
plt.legend()

# Histogram for Total Items
plt.subplot(1, 2, 2)
for category in customer_stats['visit_frequency'].unique():
    sns.histplot(customer_stats[customer_stats['visit_frequency'] == category]['total_items'], bins=30,
                 kde=True, label=category, alpha=0.5)
plt.title('Distribution of Total Items by Visit Frequency')
plt.xlabel('Total Items')
plt.ylabel('Frequency')
plt.legend()

plt.tight_layout()
plt.show()

# Create subplots for frequency plots
plt.figure(figsize=(18, 6))

# Frequency plot for Spending Category
plt.subplot(1, 3, 1)
sns.countplot(x='spending_category', data=customer_stats, palette='Set1')
plt.title('Frequency of Customers by Spending Category')
plt.xlabel('Spending Category')
plt.ylabel('Number of Customers')

# Frequency plot for Visit Frequency
plt.subplot(1, 3, 2)
sns.countplot(x='visit_frequency', data=customer_stats, palette='Set2')
plt.title('Frequency of Customers by Visit Frequency')
plt.xlabel('Visit Frequency')
plt.ylabel('Number of Customers')

# Frequency plot for Time Spent Category
plt.subplot(1, 3, 3)
sns.countplot(x='time_spent_category', data=customer_stats, palette='Set3')
plt.title('Frequency of Customers by Time Spent Category')
plt.xlabel('Time Spent Category')
plt.ylabel('Number of Customers')

plt.tight_layout()
plt.show()
# Overlayed histograms for frequency plots
plt.figure(figsize=(12, 8))

# Frequency plot for Spending Category
sns.countplot(x='spending_category', data=customer_stats, palette='Set1', hue='visit_frequency')
plt.title('Frequency of Customers by Spending Category')
plt.xlabel('Spending Category')
plt.ylabel('Number of Customers')
plt.legend(title='Visit Frequency')

plt.tight_layout()
plt.show()





