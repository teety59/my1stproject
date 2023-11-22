from flask import Flask, render_template, request, redirect, session
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

    # Create or load the sales DataFrame
    try:
        df_sales = pd.read_excel("sales.xlsx")
    except FileNotFoundError:
        df_sales = pd.DataFrame(columns=["Time", "Item", "Amount", "Price","Total"])
        

    # Append the new transaction to the sales DataFrame
    total = float(price)*int(amount)
    new_transaction = {"Time": current_time, "Item": item, "Amount": amount, "Price": price,"Total":total}
    x = pd.DataFrame(new_transaction,index =[0])
    print(x)    
    df_sales = pd.concat([df_sales, x], ignore_index=True)

    # Save the updated sales DataFrame back to the "sales.xlsx" file
    df_sales.to_excel("sales.xlsx", index=False)
def get_stock_data():
    try:
        df_stock = pd.read_excel("stock.xlsx")
        stock_data = list(zip(df_stock["Item"].tolist(), df_stock["Price"].tolist()))
    except FileNotFoundError:
        stock_data = []
    return stock_data
def get_sorted_sales_data():
    try:
        df_sales = pd.read_excel("sales.xlsx")
        df_sales["Time"] = pd.to_datetime(df_sales["Time"])
        df_sales = df_sales.sort_values(by="Time")
        sorted_sales_data = df_sales.to_dict(orient="records")
    except FileNotFoundError:
        sorted_sales_data = []
    return sorted_sales_data

@app.route("/")
def index():
    if 'username' in session:
        stock_data = get_stock_data()
        return render_template("index.html", stock_data=stock_data)
    else:
        return redirect("/login")



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
