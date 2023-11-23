from flask import Flask, render_template, request, redirect, session
import mysql.connector
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.secret_key = "aa123456"  # Change this to a random secret key

# Hardcoded username and password
VALID_USERNAME = "teety"
VALID_PASSWORD = "aa123456"

def update_sales_data(item, amount, price):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # Connect to the MariaDB server
    connection = mysql.connector.connect(
        user='teety',
        password='top38759',
        host='192.168.1.22',  # Replace with your actual database host
        database='stock',
        charset='utf8mb4',  # Set the character set to utf8mb4
        collation='utf8mb4_unicode_ci'  # Set the collation to utf8mb4_unicode_ci
    )

    try:
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Insert the new transaction into the 'sales' table
        query = "INSERT INTO sales (Time, Item, Amount, Price, Total) VALUES (%s, %s, %s, %s, %s)"
        total = float(price) * int(amount)
        data = (current_time, item, amount, price, total)
        cursor.execute(query, data)

        # Commit the changes to the database
        connection.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_sorted_sales_data():
    try:
        # Connect to the MariaDB server
        connection = mysql.connector.connect(
            user='teety',
            password='top38759',
            host='192.168.1.22',  # Replace with your actual database host
            database='stock',
            charset='utf8mb4',  # Set the character set to utf8mb4
            collation='utf8mb4_unicode_ci'  # Set the collation to utf8mb4_unicode_ci
        )

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Retrieve sorted sales data from the 'sales' table
        query = "SELECT * FROM sales"
        cursor.execute(query)
        result = cursor.fetchall()

        # Convert the result to a list of dictionaries
        columns = ["Time", "Item", "Amount", "Price", "Total"]
        sorted_sales_data = [dict(zip(columns, row)) for row in result]

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sorted_sales_data = []

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

    return sorted_sales_data

@app.route("/")
def index():
    if 'username' in session:
        # Get the listitem data from the 'listitem' table
        connection = mysql.connector.connect(
            user='teety',
            password='top38759',
            host='192.168.1.22',  # Replace with your actual database host
            database='stock',
            charset='utf8mb4',  # Set the character set to utf8mb4
            collation='utf8mb4_unicode_ci'  # Set the collation to utf8mb4_unicode_ci
        )
        
        stock_data_query = "SELECT * FROM listitem"
        stock_data = pd.read_sql(stock_data_query, connection)
        stock_data = stock_data[['Item', 'Price']].values.tolist()
        print(stock_data)

        return render_template("index.html", stock_data=stock_data)
    else:
        return redirect("/login")

# ... (rest of your routes remain unchanged)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        entered_username = request.form['username']
        entered_password = request.form['password']

        # Check if entered credentials are valid
        if entered_username == VALID_USERNAME and entered_password == VALID_PASSWORD:
            session['username'] = entered_username
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/login")

@app.route("/submit", methods=["POST"])
def submit():
    if 'username' not in session:
        return redirect("/login")

    item = request.form.get("item")
    amount = request.form.get("amount")
    price = request.form.get("price")
    

    # Update the sales data
    update_sales_data(item, amount, price)
    
    return redirect("/")
@app.route("/dashboard")
def dashboard():
    if 'username' not in session:
        return redirect("/login")

    # Get sorted sales data
    sorted_sales_data = get_sorted_sales_data()

    return render_template("dashboard.html", sales_data=sorted_sales_data)

@app.route("/stock")
def stock():
    # Get sorted sales data
    stock_data = pd.read_excel('stock.xlsx',sheet_name='Stock')  # Replace this with your actual stock data
    
    # Convert 'stock' column to integers
    stock_data['stock'] = stock_data['stock'].dropna().astype(int)

    return render_template("stock.html", stock=stock_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
