import uuid
#from typing import List, Dict, Optional



# Query 1: Place a new order for an item and quantity
# Query 2 view all orders places for a particular item
# Qurery 4: Find how many orders placed for the item using item_id

def place_order(inventory_items: list, item_id: str, quantity: int):
    # find item 
    item = find_inventory_item_by_item_id(inventory_items, item_id)
    #check the existing nventory for the item
    if item:
        if item["quantity"] >= quantity:
            orders.append(
                {
                    "order_id": str(uuid.uuid4())
                }
            )
    # if we have enough inventory then reduce the inventory

    #then place order

def find_orders_by_item_id():
    pass

def count_orders_by_item():
    pass

def find_inventory_item_by_item_id(inventory_list: list, item_id: str):
    for item in inventory_list:
        if item["item_id"] == item_id:
            return item
    return None

def update_inventory_item():
    pass