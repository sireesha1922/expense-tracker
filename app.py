import os
from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "secret123"

# -------- MONGODB --------
uri = "mongodb+srv://sireeshaerikela_db_user:Siri%40123%24@cluster0.ms3havz.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['expense_db']
users_collection = db['users']
expenses_collection = db['expenses']

# -------- HOME --------
@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')

    data = list(expenses_collection.find({'user': session['user']}))

    # FILTER
    category = request.args.get("category")
    month = request.args.get("month")

    if category:
        data = [d for d in data if d["category"] == category]

    if month:
        data = [d for d in data if d["date"].startswith(month)]

    total = sum(d["amount"] for d in data)

    # CATEGORY
    category_total = {}
    for d in data:
        category_total[d["category"]] = category_total.get(d["category"], 0) + d["amount"]

    # MONTH
    month_total = {}
    for d in data:
        m = d["date"][:7]
        month_total[m] = month_total.get(m, 0) + d["amount"]

    top_category = max(category_total, key=category_total.get) if category_total else None
    top_month = max(month_total, key=month_total.get) if month_total else None

    return render_template("index.html",
        expenses=data,
        total=total,
        category_total=category_total,
        month_total=month_total,
        top_category=top_category,
        top_month=top_month
    )

# -------- ADD --------
@app.route('/add', methods=['POST'])
def add():
    if 'user' not in session:
        return redirect('/login')

    expenses_collection.insert_one({
        "user": session['user'],
        "amount": float(request.form["amount"]),
        "category": request.form["category"],
        "date": request.form["date"]
    })

    return redirect('/')

# -------- DELETE --------
@app.route('/delete/<int:index>')
def delete(index):
    if 'user' not in session:
        return redirect('/login')

    data = list(expenses_collection.find({'user': session['user']}))

    if index < len(data):
        expenses_collection.delete_one({"_id": data[index]["_id"]})

    return redirect('/')

# -------- EDIT --------
@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    if 'user' not in session:
        return redirect('/login')

    data = list(expenses_collection.find({'user': session['user']}))

    if request.method == 'POST':
        expenses_collection.update_one(
            {"_id": data[index]["_id"]},
            {"$set": {
                "amount": float(request.form["amount"]),
                "category": request.form["category"],
                "date": request.form["date"]
            }}
        )
        return redirect('/')

    return render_template("edit.html", e=data[index])

# -------- REGISTER --------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not users_collection.find_one({"username": username}):
            users_collection.insert_one({"username": username, "password": password})
            return redirect('/login')

        return "User already exists"

    return render_template("register.html")

# -------- LOGIN --------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({"username": username, "password": password})

        if user:
            session['user'] = username
            return redirect('/')

    return render_template("login.html")

# -------- LOGOUT --------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# -------- RUN --------
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
