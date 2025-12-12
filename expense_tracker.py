"""
Smart Expense Tracker
File: expense_tracker.py
Mobile-friendly: works in Pydroid3 / QPython / Termux
Storage: expenses.json (in same folder)
"""

import json
import os
from datetime import datetime
import csv

DB_FILE = "expenses.json"

# ---------- Utility functions ----------
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)

def parse_date(text):
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except Exception:
            pass
    raise ValueError("Invalid date format. Use YYYY-MM-DD")

# ---------- Core features ----------
def add_expense():
    print("\n--- Add Expense ---")
    try:
        date_text = input("Date (YYYY-MM-DD) [leave blank for today]: ").strip()
        date = datetime.today().date() if date_text == "" else parse_date(date_text)
        title = input("Title: ").strip()
        category = input("Category: ").strip() or "Other"
        amount = float(input("Amount: ").strip())
        note = input("Note (optional): ").strip()
    except ValueError as e:
        print("Invalid input:", e)
        return

    record = {
        "id": int(datetime.now().timestamp()*1000),
        "date": str(date),
        "title": title,
        "category": category,
        "amount": amount,
        "note": note
    }
    data = load_data()
    data.append(record)
    save_data(data)
    print("Expense added successfully!")

def view_all():
    print("\n--- All Expenses ---")
    data = load_data()
    if not data:
        print("No expenses yet.")
        return
    total = 0
    for r in sorted(data, key=lambda x: x["date"], reverse=True):
        print(f'{r["date"]} | {r["category"]:<10} | ₹{r["amount"]:.2f} | {r["title"]} | {r["note"]}')
        total += r["amount"]
    print(f"Total spent: ₹{total:.2f}")

def monthly_summary():
    print("\n--- Monthly Summary ---")
    y = input("Year (YYYY): ").strip()
    m = input("Month (1-12): ").strip()
    today = datetime.today()
    year = int(y) if y else today.year
    month = int(m) if m else today.month

    data = load_data()
    filtered = [r for r in data if datetime.fromisoformat(r["date"]).year == year and datetime.fromisoformat(r["date"]).month == month]

    if not filtered:
        print("No records.")
        return

    total = sum(r["amount"] for r in filtered)
    by_cat = {}
    for r in filtered:
        by_cat[r["category"]] = by_cat.get(r["category"], 0) + r["amount"]

    print(f"Summary for {year}-{month:02d}")
    for cat, amt in by_cat.items():
        print(f"{cat}: ₹{amt:.2f} ({amt/total*100:.1f}%)")
    print("Total:", total)

def search():
    print("\n--- Search ---")
    q = input("Search text: ").strip().lower()
    data = load_data()
    result = [r for r in data if q in r["title"].lower() or q in r["category"].lower() or q in r["date"]]
    if not result:
        print("No match.")
        return
    for r in result:
        print(f'{r["date"]} | {r["category"]} | {r["title"]} | ₹{r["amount"]}')

def delete():
    print("\n--- Delete Expense ---")
    try:
        id_num = int(input("Enter ID: ").strip())
    except:
        print("Invalid ID.")
        return
    data = load_data()
    new_data = [r for r in data if r["id"] != id_num]
    if len(new_data) == len(data):
        print("ID not found.")
    else:
        save_data(new_data)
        print("Deleted successfully!")

def export_csv():
    print("\n--- Export CSV ---")
    fname = "expenses_export.csv"
    data = load_data()
    if not data:
        print("No data to export.")
        return
    with open(fname, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "date", "title", "category", "amount", "note"])
        for r in data:
            writer.writerow([r["id"], r["date"], r["title"], r["category"], r["amount"], r["note"]])
    print("Exported to", fname)

# ---------- Menu ----------
def menu():
    while True:
        print("\n=== Smart Expense Tracker ===")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Monthly Summary")
        print("4. Search")
        print("5. Delete Expense")
        print("6. Export CSV")
        print("7. Exit")
        choice = input("Choose 1-7: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_all()
        elif choice == "3":
            monthly_summary()
        elif choice == "4":
            search()
        elif choice == "5":
            delete()
        elif choice == "6":
            export_csv()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()
