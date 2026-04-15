from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "secret123"

# ✅ MongoDB Connection (FINAL WORKING)
uri = "mongodb+srv://sireeshaerikela_db_user:Siri%40123%24@cluster0.ms3havz.mongodb.net/expense_db?retryWrites=true&w=majority"

client = MongoClient(uri, serverSelectionTimeoutMS=5000)
db = client["expense_db"]

users_collection = db["users"]
expenses_collection = db["expenses"]

# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing = users_collection.find_one({"username": username})
        if existing:
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
            return redirect("/dashboard")
        else:
            return "Invalid login!"

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    user = session["user"]

    expenses = list(expenses_collection.find({"user": user}))
    total = sum(int(exp["amount"]) for exp in expenses)

    return render_template("dashboard.html", expenses=expenses, total=total)

# ---------------- ADD EXPENSE ----------------
@app.route("/add", methods=["POST"])
def add():
    if "user" not in session:
        return redirect("/login")

    amount = request.form["amount"]
    category = request.form["category"]

    expenses_collection.insert_one({
        "user": session["user"],
        "amount": amount,
        "category": category
    })

    return redirect("/dashboard")

# ---------------- DELETE ----------------
@app.route("/delete/<id>")
def delete(id):
    expenses_collection.delete_one({"_id": ObjectId(id)})
    return redirect("/dashboard")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
