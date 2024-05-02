
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
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
with open("supermarket.csv", "r") as file:
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

# Analyzing department visits per customer using a heatmap
department_pivot = pd.pivot_table(df, values='price', index='customer_id', columns='department', aggfunc='size',
                                  fill_value=0)
plt.figure(figsize=(12, 10))
sns.heatmap(department_pivot, cmap='viridis', cbar_kws={'label': 'Number of Visits'})
plt.title('Heatmap of Department Visits per Customer')
plt.xlabel('Department')
plt.ylabel('Customer ID')
plt.show()

# Feature engineering
# Grouping data by customer_id and calculating aggregate statistics
customer_stats = df.groupby('customer_id').agg(
    total_spent=pd.NamedAgg(column='price', aggfunc='sum'),
    total_items=pd.NamedAgg(column='price', aggfunc='size'),
    avg_spent_per_visit=pd.NamedAgg(column='price', aggfunc='mean'),
    total_time=pd.NamedAgg(column='time_elapsed', aggfunc='sum'),
    avg_time_between_scans=pd.NamedAgg(column='time_elapsed', aggfunc='mean')
)

# Department visit counts
department_visits = pd.get_dummies(df['department']).groupby(df['customer_id']).sum()

# Combining all features into a single DataFrame
features_df = pd.concat([customer_stats, department_visits], axis=1)

# Handling missing values if any - This can be necessary if some customers have no data for specific departments
features_df.fillna(0, inplace=True)

print(features_df.head())

# Scale the features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features_df)

# Applying PCA
pca = PCA(n_components=0.95)  # Adjust this to capture the desired amount of variance
principal_components = pca.fit_transform(features_scaled)

# Analyzing the amount of variance that each PC explains
explained_variance = pca.explained_variance_ratio_
print("Explained Variance: ", explained_variance)

# Plotting the cumulative variance
plt.figure()
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('Explained Variance by PCA Components')
plt.show()

# Checking the contribution of each feature to the principal components
print("PCA Component weights:\n", pca.components_)
plt.figure(figsize=(8, 6))
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('PCA Cumulative Explained Variance')
plt.grid(True)
plt.show()

# Select number of components you wish to visualize
num_components = 5

fig, axes = plt.subplots(num_components, 1, figsize=(12, 10))
fig.tight_layout(pad=3.0)

for i in range(num_components):
    components = pca.components_[i]
    ax = axes[i]
    ax.bar(range(len(components)), components)
    ax.set_title(f'Component {i+1} Loadings')
    ax.set_xticks(range(len(components)))
    ax.set_xticklabels(features_df.columns, rotation=90)
plt.show()
