import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Connection string
uri = "mongodb+srv://sireeshaerikela_db_user:Siri%40123%24@cluster0.ms3havz.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['expense_db']
users_collection = db['users']

@app.route('/')
def home():
    return render_template('login.html') # Loads your visual login page

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not users_collection.find_one({'username': username}):
            users_collection.insert_one({'username': username, 'password': password})
            return redirect('/login')
        return "User already exists!"
    return render_template('register.html') # Loads your visual register page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if users_collection.find_one({'username': username, 'password': password}):
            return "Login Successful!"
    return render_template('login.html') # Loads your visual login page

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
