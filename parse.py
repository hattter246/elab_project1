import csv

# Add the customer_id and handling full transactions
file_path = '/Users/cornelius/Downloads/supermarket.csv'

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


def parse_csv_row(row, customer_id):
    transactions = []
    for item in row.split(','):
        dept_code, time_elapsed, price = item.strip().split()
        transactions.append({
            "customer_id": customer_id,
            "department": department_mapping[dept_code],
            "time_elapsed": int(time_elapsed),
            "price": float(price)
        })
    return transactions


all_transactions = []

with open(file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for customer_id, row in enumerate(reader):
        transactions = parse_csv_row(row[0], customer_id)
        all_transactions.extend(transactions)

print(all_transactions[:5])