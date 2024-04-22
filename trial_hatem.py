import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

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
with open("supermarket.csv", "r") as file:
    parsed_data = []
    na_count = 0  # Initialize NA count
    for line in file:
        transactions = line.strip().split(", ")
        parsed_transactions = []
        for transaction in transactions:
            transaction_data = transaction.split()
            if len(transaction_data) == 3:
                department_code, time_elapsed, price = transaction_data
                # Remove the comma from the price before converting it to float
                price = price.rstrip(',')
                department = department_mapping.get(int(department_code))
                if department is None:
                    print("Invalid department code:", department_code)
                    continue
                try:
                    time_elapsed = int(time_elapsed)
                    price = float(price)
                except ValueError:
                    print("Invalid time or price format:", transaction_data)
                    continue
                parsed_transactions.append((department, time_elapsed, price))
            else:
                print("Invalid transaction format:", transaction_data)
                na_count += 1  # Increment NA count for invalid transactions
        # Check for NAs in parsed transactions
        if len(parsed_transactions) == 0:
            print("No valid transactions found in line:", line.strip())
            na_count += 1  # Increment NA count if no valid transactions found
        else:
            parsed_data.append(parsed_transactions)

# Create a DataFrame from the parsed data
df_parsed = pd.DataFrame({"parsed_transactions": parsed_data})

# Save the DataFrame to a CSV file
df_parsed.to_csv("parsed_supermarket_data.csv", index=False)

# Display the preprocessed dataframe
print(df_parsed.head())

# Print the total count of NAs
print("Total count of NAs:", na_count)



# Load the parsed supermarket data
df_parsed = pd.read_csv("parsed_supermarket_data.csv")

# Initialize variables for features
total_time_spent = defaultdict(int)  # Total time spent in the store per customer
total_items_scanned = defaultdict(int)  # Total number of items scanned per customer
total_amount_spent = defaultdict(float)  # Total amount spent per customer
visit_count = defaultdict(int)  # Frequency of visits per customer
department_visits = defaultdict(lambda: defaultdict(int))  # Department visit counts per customer

# Iterate through each row in the DataFrame
for index, row in df_parsed.iterrows():
    visits = eval(row['parsed_transactions'])  # Convert string representation to list of tuples
    customer_id = index  # Assuming index represents customer ID

    # Initialize variables for each visit
    visit_time = 0
    last_scan_time = 0
    total_scans = 0
    total_amount = 0

    # Iterate through each transaction in the visit
    for visit in visits:
        if len(visit) != 3:
            print("Invalid transaction format:", visit)
            continue
        department, time_elapsed, price = visit
        total_scans += 1
        total_amount += price

        # Update department visit count
        department_visits[customer_id][department] += 1

        # Update total time spent in the store
        visit_time += time_elapsed

        # Calculate average time between scans
        if last_scan_time != 0:
            time_between_scans = time_elapsed - last_scan_time
            total_time_spent[customer_id] += time_between_scans
        last_scan_time = time_elapsed

    # Update total items scanned and total amount spent for the customer
    total_items_scanned[customer_id] += total_scans
    total_amount_spent[customer_id] += total_amount

    # Update visit count for the customer
    visit_count[customer_id] += 1

# Calculate average time between scans
average_time_between_scans = {customer_id: total_time_spent[customer_id] / total_items_scanned[customer_id]
                              for customer_id in total_items_scanned}

# Create a DataFrame for additional features
df_features = pd.DataFrame({
    'customer_id': list(total_items_scanned.keys()),
    'total_time_spent': list(total_time_spent.values()),
    'total_items_scanned': list(total_items_scanned.values()),
    'total_amount_spent': list(total_amount_spent.values()),
    'visit_count': list(visit_count.values()),
    'average_time_between_scans': list(average_time_between_scans.values())
})

# Display the additional features DataFrame
print(df_features.head())

# Save the additional features DataFrame to a CSV file
df_features.to_csv("additional_features.csv", index=False)



# Load the additional features DataFrame
df_features = pd.read_csv("additional_features.csv")

# Plot boxplots for each feature
plt.figure(figsize=(16, 8))
plt.subplot(2, 3, 1)
sns.boxplot(y=df_features['total_time_spent'])
plt.title('Boxplot of Total Time Spent')

plt.subplot(2, 3, 2)
sns.boxplot(y=df_features['total_items_scanned'])
plt.title('Boxplot of Total Items Scanned')

plt.subplot(2, 3, 3)
sns.boxplot(y=df_features['total_amount_spent'])
plt.title('Boxplot of Total Amount Spent')

plt.subplot(2, 3, 4)
sns.boxplot(y=df_features['visit_count'])
plt.title('Boxplot of Visit Count')

plt.subplot(2, 3, 5)
sns.boxplot(y=df_features['average_time_between_scans'])
plt.title('Boxplot of Average Time Between Scans')

plt.tight_layout()
plt.show()

# Plot histograms for each feature on a grid
plt.figure(figsize=(16, 8))
plt.subplot(2, 3, 1)
sns.histplot(df_features['total_time_spent'], bins=30, kde=True)
plt.title('Distribution of Total Time Spent')

plt.subplot(2, 3, 2)
sns.histplot(df_features['total_items_scanned'], bins=30, kde=True)
plt.title('Distribution of Total Items Scanned')

plt.subplot(2, 3, 3)
sns.histplot(df_features['total_amount_spent'], bins=30, kde=True)
plt.title('Distribution of Total Amount Spent')

plt.subplot(2, 3, 4)
sns.histplot(df_features['visit_count'], bins=30, kde=True)
plt.title('Distribution of Visit Count')

plt.subplot(2, 3, 5)
sns.histplot(df_features['average_time_between_scans'], bins=30, kde=True)
plt.title('Distribution of Average Time Between Scans')

plt.tight_layout()
plt.show()

# Frequency plot for department visits
department_counts = defaultdict(int)
for customer_id, visits in department_visits.items():
    for department, count in visits.items():
        department_counts[department] += count

departments = list(department_counts.keys())
frequencies = list(department_counts.values())

plt.figure(figsize=(10, 6))
sns.barplot(x=departments, y=frequencies, palette='viridis')
plt.title('Frequency of Department Visits', fontsize=14)
plt.xlabel('Department', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
plt.show()

