import json
import os
from datetime import datetime

ORDER_FILE = "Database/orders.json"  

def loadOrders():
    if not os.path.exists(ORDER_FILE):
        return []
    with open(ORDER_FILE) as file:
        return json.load(file)

def saveOrders(orders):
    with open(ORDER_FILE, "w") as file:
        json.dump(orders, file, indent=4)

def generatingBill():
    orders = loadOrders()

    
    date_str = input("Enter date to filter orders (YYYY-MM-DD) or press Enter for all: ").strip()
    if date_str:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format.")
            return
        filtered = []
        for o in orders:
            dt = o.get("datetime", "")  
            if dt.startswith(date_str):
                filtered.append(o)
    else:
        filtered = orders

    
    pending_orders = [o for o in filtered if o.get("status") != "paid"]

    if not pending_orders:
        print("No pending orders to bill for that date.")
        return

    print("\n------ Pending Orders ------")
    for o in pending_orders:
        dt_display = o.get("datetime", "N/A")
        print(f"Order ID: {o['order_id']}, Customer: {o['customer_name']}, Amount: {o['total']}, DateTime: {dt_display}")

    try:
        orderId = int(input("\nEnter Order ID to generate bill: "))
    except ValueError:
        print("Invalid Order ID.")
        return

   
    selected_order = None
    for o in pending_orders:
        if o["order_id"] == orderId:
            selected_order = o
            break

    if not selected_order:
        print("Order not found or already paid.")
        return

    subTotal = selected_order["total"]
    taxRate = 0.05
    tax = subTotal * taxRate
    discount = 0.0

    applyDiscount = input("Apply discount? (y/n): ").lower()
    if applyDiscount == "y":
        try:
            discount = float(input("Enter discount amount: "))
        except ValueError:
            print("Invalid discount input. No discount applied.")
            discount = 0.0

    grandTotal = subTotal + tax - discount

    print("\n====== CUSTOMER BILL ======")
    print(f"Customer    : {selected_order['customer_name']}")
    print(f"Order ID    : {selected_order['order_id']}")
    print(f"Date/Time   : {selected_order.get('datetime', 'N/A')}")
    print("-" * 30)
    for item in selected_order.get('items', []):
        line_total = item.get("price", 0) * item.get("quantity", 0)
        print(f"{item.get('name')} x {item.get('quantity')} = {line_total:.2f}")
    print("-" * 30)
    print(f"Subtotal    : {subTotal:.2f}")
    print(f"Tax (5%)    : {tax:.2f}")
    print(f"Discount    : -{discount:.2f}")
    print(f"Grand Total : {grandTotal:.2f}")
    print("-" * 30)

    confirm = input("Mark order as paid? (y/n): ").lower()
    if confirm == "y":
        
        for o in orders:
            if o["order_id"] == selected_order["order_id"]:
                o["status"] = "paid"
                break
        saveOrders(orders)
        print("Payment completed. Order marked as paid.")
    else:
        print("Order not marked as paid.")
