import pandas as pd
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
parsed_data = []
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
                        "department": department,
                        "time_elapsed": time_elapsed,
                        "price": price
                    })
                except ValueError:
                    print("Error converting data:", parts)

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
