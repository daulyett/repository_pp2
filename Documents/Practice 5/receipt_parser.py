import re
import json

# Read raw receipt file
with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

print("----- RAW RECEIPT -----")
print(text)
print("------------------------\n")


#1 Extract all prices (example: 123.45 or 1 234.50)
prices = re.findall(r"\d+\.\d{2}", text)
prices = [float(p) for p in prices]

print("Prices:", prices)


#2 Extract product names (example: lines before price)
products = re.findall(r"([A-Za-zА-Яа-я\s]+)\s+\d+\.\d{2}", text)
print("Products:", products)


#3 Calculate total amount
total = sum(prices)
print("Calculated Total:", total)


#4 Extract date (example: 12.03.2026)
date_match = re.search(r"\d{2}\.\d{2}\.\d{4}", text)
date = date_match.group() if date_match else None
print("Date:", date)


#5 Extract time (example: 14:32)
time_match = re.search(r"\d{2}:\d{2}", text)
time = time_match.group() if time_match else None
print("Time:", time)


#6 Extract payment method (CARD / CASH)
payment_match = re.search(r"(CARD|CASH|VISA|MASTERCARD)", text, re.IGNORECASE)
payment_method = payment_match.group() if payment_match else "Unknown"
print("Payment method:", payment_method)


#7 Create structured JSON output
receipt_data = {
    "date": date,
    "time": time,
    "products": products,
    "prices": prices,
    "total": total,
    "payment_method": payment_method
}

print("\n----- STRUCTURED OUTPUT -----")
print(json.dumps(receipt_data, indent=4, ensure_ascii=False))