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
        cat = e["category"]
        category_total[cat] = category_total.get(cat, 0) + int(e["amount"])

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
