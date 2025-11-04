#!/usr/bin/env python3
"""
A simple inventory management system.

This module provides basic functions to add, remove, and track items
in a simple dictionary-based inventory (stock_data).
"""

import json
# FIX: Removed unused 'logging' import (Flake8: F401, Pylint: W0611)
from datetime import datetime


def add_item(stock_data, item="default", qty=0, logs=None):
    """
    Adds a specified quantity of an item to the stock.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to add.
        qty (int): The quantity to add.
        logs (list, optional): A log list. Defaults to None.
    """
    # FIX: (Pylint: W0102) Use 'None' default for mutable arguments
    if logs is None:
        logs = []

    if not item:
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    # FIX: (Pylint: C0209) Use f-string for cleaner formatting
    logs.append(f"{str(datetime.now())}: Added {qty} of {item}")


def remove_item(stock_data, item, qty):
    """
    Removes a specified quantity of an item from the stock.

    If the quantity drops to 0 or below, the item is removed.
    Safely handles attempts to remove non-existent items.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to remove.
        qty (int): The quantity to remove.
    """
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    # FIX: (Flake8: E722, Pylint: W0702, Bandit: B110)
    # Replaced bare 'except:' with specific 'KeyError'.
    except KeyError:
        # It's better to log or print this than 'pass' silently.
        print(f"Warning: Item '{item}' not in stock. No items removed.")


def get_qty(stock_data, item):
    """
    Gets the current quantity of a specific item.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to check.

    Returns:
        int: The quantity of the item, or 0 if not found.
    """
    # Added error handling for robustness
    try:
        return stock_data[item]
    except KeyError:
        return 0


def load_data(file="inventory.json"):
    """
    Loads the inventory from a JSON file.

    Args:
        file (str, optional): The file to load from. Defaults to "inventory.json".

    Returns:
        dict: The loaded inventory data. Returns empty dict if file not found.
    """
    # FIX: (Pylint: R1732) Use 'with' for resource management
    # FIX: (Pylint: W1514) Specify 'encoding'
    # FIX: (Pylint: W0603) Removed 'global' statement. Function now returns data.
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        print(f"Info: No '{file}' found. Starting with empty inventory.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode '{file}'. Starting with empty inventory.")
        return {}


def save_data(stock_data, file="inventory.json"):
    """
    Saves the current inventory to a JSON file.

    Args:
        stock_data (dict): The inventory dictionary to save.
        file (str, optional): The file to save to. Defaults to "inventory.json".
    """
    # FIX: (Pylint: R1732) Use 'with' for resource management
    # FIX: (Pylint: W1514) Specify 'encoding'
    try:
        with open(file, "w", encoding="utf-8") as f:
            f.write(json.dumps(stock_data, indent=4))
    except IOError as e:
        print(f"Error: Could not save data to '{file}': {e}")


def print_data(stock_data):
    """
    Prints a formatted report of all items and their quantities.

    Args:
        stock_data (dict): The inventory dictionary.
    """
    print("\n--- Items Report ---")
    if not stock_data:
        print("  Inventory is empty.")
    else:
        for i in stock_data:
            print(f"  {i} -> {stock_data[i]}")
    print("----------------------\n")


def check_low_items(stock_data, threshold=5):
    """
    Finds all items with a quantity below a given threshold.

    Args:
        stock_data (dict): The inventory dictionary.
        threshold (int, optional): The low-stock threshold. Defaults to 5.

    Returns:
        list: A list of item names that are below the threshold.
    """
    return [i for i in stock_data if stock_data[i] < threshold]


def main():
    """
    Main function to run the inventory management tasks.
    """
    # FIX: (Pylint: W0603) 'stock_data' is now a local variable,
    # initialized here and passed to functions.
    stock_data = load_data()

    # Note: 'add_item' no longer passes in the 'logs' list, so it will
    # create a new one each time. To share a log, you would do:
    # my_logs = []
    # add_item(stock_data, "apple", 10, logs=my_logs)
    add_item(stock_data, "apple", 10)
    add_item(stock_data, "banana", 15)

    # This call demonstrates the original bug.
    # The 'ten' string will cause a TypeError, which is now unhandled
    # because 'remove_item' only catches 'KeyError'. This is correct,
    # as this is a *programming error* that should be fixed.
    try:
        add_item(stock_data, 123, "ten")  # invalid types
    except TypeError:
        print("Error: Invalid types provided to add_item.")

    remove_item(stock_data, "apple", 3)
    remove_item(stock_data, "orange", 1)  # Will trigger 'KeyError' warning

    print(f"Apple stock: {get_qty(stock_data, 'apple')}")
    print(f"Orange stock: {get_qty(stock_data, 'orange')}")
    print(f"Low items: {check_low_items(stock_data)}")

    save_data(stock_data)
    
    # Reload the data to ensure saving and loading works
    stock_data = load_data()
    print_data(stock_data)

    # FIX: (Pylint: W0123, Bandit: B307) Dangerous 'eval' call removed.
    print("Inventory check complete.")


# FIX: Use standard entry point guard
if __name__ == "__main__":
    main()