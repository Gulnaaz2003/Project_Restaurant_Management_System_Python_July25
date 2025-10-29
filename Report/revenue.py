import json 
import os 
from datetime import datetime
from Logs.log import error_logs


def monthlyReport():
    try:
        os.makedirs("Database", exist_ok=True)
        
        orders_file = "Database/orders.json"
        if os.path.exists(orders_file):
            with open (orders_file, "r") as f:
                orders = json.load(f)
        
        else:
            print("No orders found.")
            return
        
        if not orders:
            print("No orders found.")
            return

        month_input = input("Enter month to generate report (YYYY-MM): ").strip()
        try:
            datetime.strptime(month_input, "%Y-%m")
        except ValueError:
            print("Invalid month format. Use YYYY-MM (e.g., 2025-10)")
            return

        report_data = {}
        grand_total = 0.0
        total_orders = 0

        for order in orders:
            order_date = order["datetime"][:10] 
            if not order_date.startswith(month_input):
                continue

            total = float(order["total"])
            report_data.setdefault(order_date, {"total_sales": 0.0, "order_count": 0})
            report_data[order_date]["total_sales"] += total
            report_data[order_date]["order_count"] += 1
            grand_total += total
            total_orders += 1

        if not report_data:
            print(f"No sales found for month {month_input}.")
            return

        print(f"\n------ Monthly Sales Report for {month_input} ------")
        print("{:<12} {:<15} {:<10}".format("Date", "Total Sales (₹)", "Orders"))
        print("-" * 40)
        for date, data in sorted(report_data.items()):
            print("{:<12} {:<15} {:<10}".format(date, f"{data['total_sales']:.2f}", data["order_count"]))
        print("-" * 40)
        print(f"Grand Total: ₹{grand_total:.2f} | Total Orders: {total_orders}")

        report_file = f"Database/report_{month_input}.json"
        with open(report_file, "w") as f:
            json.dump({
                "month": month_input,
                "grand_total": grand_total,
                "total_orders": total_orders,
                "details": report_data
            }, f, indent=4)

        print(f"\nReport saved successfully → {report_file}")

    except Exception as e:
        error_logs(e)