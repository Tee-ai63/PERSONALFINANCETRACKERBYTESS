import streamlit as st
import csv
from datetime import datetime
import matplotlib.pyplot as plt

FILE_NAME = "finance_data.csv"

# Initialize the file if it doesn't exist
def init_file():
    try:
        with open(FILE_NAME, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Type", "Category/Source", "Amount"])
    except FileExistsError:
        pass

init_file()

# Add a new record
def add_record(record_type, category, amount):
    date = datetime.now().strftime("%Y-%m-%d")
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, record_type, category, amount])

# Show summary
def show_summary():
    total_income, total_expense = 0, 0
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            if not row:
                continue
            if row[1] == "Income":
                total_income += float(row[3])
            elif row[1] == "Expense":
                total_expense += float(row[3])

    balance = total_income - total_expense
    return total_income, total_expense, balance

# Create pie chart
def create_pie_chart(total_income, total_expense):
    values = [total_income, total_expense]
    labels = ["Income", "Expenses"]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%")
    ax.set_title("Income vs Expenses")
    return fig

# --- Streamlit UI ---

st.title("💰 Personal Finance Tracker")

# Input section
st.header("Add a Record")
record_type = st.radio("Select type:", ["Income", "Expense"])
category = st.text_input("Category/Source:")
amount = st.number_input("Amount:", min_value=0.0, step=100.0)

if st.button("Add Record"):
    if category and amount > 0:
        add_record(record_type, category, amount)
        st.success("Record added successfully!")
    else:
        st.error("Please enter a category and amount.")

# Summary section
st.header("Summary")
if st.button("Show Summary"):
    total_income, total_expense, balance = show_summary()
    st.write(f"**Total Income:** {total_income}")
    st.write(f"**Total Expense:** {total_expense}")
    st.write(f"**Balance:** {balance}")

    fig = create_pie_chart(total_income, total_expense)
    st.pyplot(fig)
    