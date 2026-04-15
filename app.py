from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "secret123"

# ✅ MongoDB Connection
uri = "mongodb+srv://sireeshaerikela_db_user:Siri%40123%24@cluster0.ms3havz.mongodb.net/expense_db?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["expense_db"]

users_collection = db["users"]
expenses_collection = db["expenses"]

# ---------------- HOME (MAIN PAGE) ----------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    user = session["user"]

    expenses = list(expenses_collection.find({"user": user}))

    total = sum(int(e["amount"]) for e in expenses)

    category_total = {}
    month_total = {}

    for e in expenses:
        # CATEGORY
        cat = e["category"]
        category_total[cat] = category_total.get(cat, 0) + int(e["amount"])

        # MONTH
        if "date" in e:
            month = e["date"][:7]
            month_total[month] = month_total.get(month, 0) + int(e["amount"])

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        category_total=category_total,
        month_total=month_total
    )

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users_collection.find_one({"username": username}):
            return "User already exists!"

        users_collection.insert_one({
            "username": username,
            "password": password
        })

        return redirect("/login")

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users_collection.find_one({
            "username": username,
            "password": password
        })

        if user:
            session["user"] = username
            return redirect("/")   # ✅ FIXED (NO dashboard)

        return "Invalid login!"

    return render_template("login.html")

# ---------------- ADD EXPENSE ----------------
@app.route("/add", methods=["POST"])
def add():
    if "user" not in session:
        return redirect("/login")

    amount = request.form["amount"]
    category = request.form["category"]
    date = request.form["date"]

    expenses_collection.insert_one({
        "user": session["user"],
        "amount": amount,
        "category": category,
        "date": date
    })

    return redirect("/")

# ---------------- DELETE ----------------
@app.route("/delete/<id>")
def delete(id):
    expenses_collection.delete_one({"_id": ObjectId(id)})
    return redirect("/")

# ---------------- EDIT ----------------
@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    expense = expenses_collection.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        date = request.form["date"]

        expenses_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "amount": amount,
                "category": category,
                "date": date
            }}
        )
        return redirect("/")

    return render_template("edit.html", e=expense)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
