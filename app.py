from flask import Flask, render_template, request, redirect, session
import json, os

app = Flask(__name__)
app.secret_key = "secret123"

# -------- USERS --------
def load_users():
    if not os.path.exists("users.json"):
        return {}
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

# -------- DATA --------
def get_file():
    return f"{session['user']}_expenses.json"

def load_data():
    file = get_file()
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)

def save_data(data):
    with open(get_file(), "w") as f:
        json.dump(data, f, indent=4)

# -------- HOME --------
@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')

    data = load_data()

    # FILTER
    selected_cat = request.args.get("category")
    selected_month = request.args.get("month")

    if selected_cat:
        data = [d for d in data if d["category"] == selected_cat]

    if selected_month:
        data = [d for d in data if d["date"].startswith(selected_month)]

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

    # INSIGHTS
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
    data = load_data()
    data.append({
        "amount": float(request.form["amount"]),
        "category": request.form["category"],
        "date": request.form["date"]
    })
    save_data(data)
    return redirect('/')

# -------- DELETE --------
@app.route('/delete/<int:i>')
def delete(i):
    data = load_data()
    if i < len(data):
        data.pop(i)
    save_data(data)
    return redirect('/')

# -------- EDIT --------
@app.route('/edit/<int:i>', methods=['GET', 'POST'])
def edit(i):
    data = load_data()

    if request.method == 'POST':
        data[i] = {
            "amount": float(request.form["amount"]),
            "category": request.form["category"],
            "date": request.form["date"]
        }
        save_data(data)
        return redirect('/')

    return render_template("edit.html", e=data[i])

# -------- AUTH --------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        users[request.form['username']] = request.form['password']
        save_users(users)
        return redirect('/login')
    return render_template("register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        u = request.form['username']
        p = request.form['password']

        if u in users and users[u] == p:
            session['user'] = u
            return redirect('/')

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)