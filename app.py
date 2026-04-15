from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "secret123"

# 🔥 MongoDB Connection (your working one)
uri = "mongodb+srv://sireeshaerikela_db_user:Siri%40123%24@cluster0.ms3havz.mongodb.net/expense_db?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["expense_db"]

users = db["users"]
expenses_collection = db["expenses"]

# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    expenses = list(expenses_collection.find({"user": session["user"]}))

    total = 0
    for expense in expenses:
        total += float(expense.get("amount", 0))

    # ✅ FIXED CATEGORY TOTAL
    category_total = {}

    for expense in expenses:
        cat = expense.get("category", "Other")
        amount = float(expense.get("amount", 0))

        if cat in category_total:
            category_total[cat] += amount
        else:
            category_total[cat] = amount

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        category_total=category_total
    )

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]

        users.insert_one({
            "username": user,
            "password": password
        })

        return redirect("/login")

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]

        found = users.find_one({
            "username": user,
            "password": password
        })

        if found:
            session["user"] = user
            return redirect("/")
        else:
            return "Invalid login"

    return render_template("login.html")

# ---------------- ADD EXPENSE ----------------
@app.route("/add", methods=["POST"])
def add():
    if "user" not in session:
        return redirect("/login")

    title = request.form["title"]
    amount = request.form["amount"]
    category = request.form["category"]

    expenses_collection.insert_one({
        "title": title,
        "amount": amount,
        "category": category,
        "user": session["user"]
    })

    return redirect("/")

# ---------------- DELETE ----------------
@app.route("/delete/<id>")
def delete(id):
    from bson.objectid import ObjectId
    expenses_collection.delete_one({"_id": ObjectId(id)})
    return redirect("/")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
