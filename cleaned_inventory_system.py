# Unused 'logging' import removed (Low Priority)
import json
from datetime import datetime

# Fixed file handling with 'with open()' (High Priority)
# Added 'encoding' (Medium Priority)
# Renamed function to snake_case (Low Priority)
# Part of refactoring to remove 'global' (Medium Priority)
def load_data(file="inventory.json"):
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
    except FileNotFoundError:
        print(f"Warning: {file} not found. Starting with empty inventory.")
        stock_data = {}
    return stock_data


# Fixed file handling with 'with open()' (High Priority)
# Added 'encoding' (Medium Priority)
# Renamed function to snake_case (Low Priority)
def save_data(stock_data, file="inventory.json"):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=4)


# Fixed dangerous default 'logs=[]' (High Priority)
# Used f-string for formatting (Low Priority)
# Renamed function to snake_case (Low Priority)
def add_item(stock_data, item="default", qty=0, logs=None):
    if logs is None:
        logs = []

    if not item:
        return

    try:
        stock_data[item] = stock_data.get(item, 0) + qty
        logs.append(f"{str(datetime.now())}: Added {qty} of {item}")
    except TypeError:
        print(f"Error: Invalid quantity '{qty}' for item '{item}'.")


# Fixed bare 'except' to 'except KeyError' (High Priority)
# Renamed function to snake_case (Low Priority)
def remove_item(stock_data, item, qty):
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        print(f"Warning: Item '{item}' not in stock, cannot remove.")
    except TypeError:
        print(f"Error: Invalid quantity '{qty}' for item '{item}'.")


# Renamed function to snake_case (Low Priority)
def get_qty(stock_data, item):
    return stock_data.get(item)


# Renamed function to snake_case (Low Priority)
def print_data(stock_data):
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])


# Renamed function to snake_case (Low Priority)
def check_low_items(stock_data, threshold=5):
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result


# Removed 'eval()' (High Priority - Security)
# Refactored to remove 'global' (Medium Priority)
def main():
    stock_data = load_data()

    add_item(stock_data, "apple", 10)
    add_item(stock_data, "banana", -2)
    add_item(stock_data, 123, "ten")

    remove_item(stock_data, "apple", 3)
    remove_item(stock_data, "orange", 1)

    print("Apple stock:", get_qty(stock_data, "apple"))
    print("Low items:", check_low_items(stock_data))

    save_data(stock_data)
    stock_data = load_data()
    print_data(stock_data)

    print("--- End of Report ---")


# Added main execution block
if __name__ == "__main__":
    main()

# Also fixed: All whitespace/formatting and missing final newline (Low Priority)