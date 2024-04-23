import csv

# Dictionary to map department codes to department names
department_mapping = {
    '1': 'Bakery & Pastry',
    '2': 'Beer & Wine',
    '3': 'Books & Magazines',
    '4': 'Candy & Chips',
    '5': 'Care & Hygiene',
    '6': 'Cereals & Spreads',
    '7': 'Cheese & Tapas',
    '8': 'Dairy & Eggs',
    '9': 'Freezer',
    '10': 'Fruit & Vegetables',
    '11': 'Household & Pet',
    '12': 'Meat & Fish',
    '13': 'Pasta & Rice',
    '14': 'Salads & Meals',
    '15': 'Sauces & Spices',
    '16': 'Soda & Juices',
    '17': 'Special Diet',
    '18': 'Vegetarian & Vegan'
}

# Function to parse each row of the CSV file
def parse_csv_row(row):
    transactions = []
    for item in row.split(','):
        dept_code, time_elapsed, price = item.strip().split()
        transactions.append((department_mapping[dept_code], int(time_elapsed), float(price)))
    return transactions

# Path to the CSV file
file_path = r"C:\Users\Adam\OneDrive\Pulpit\Period 5\eLab II\supermarket\supermarket.csv"

# Reading and parsing the CSV file
with open(file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        transactions = parse_csv_row(row[0])
        # print("Customer transactions:")
        for transaction in transactions:
            print(f"{transaction[0]}, Time: {transaction[1]} s, Price: €{transaction[2]}")
