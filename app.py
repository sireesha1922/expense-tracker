import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB using the URI you added to Render
client = MongoClient(os.environ.get('MONGO_URI'))
db = client['expense_db']
users_collection = db['users']

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Save to MongoDB
        if not users_collection.find_one({'username': username}):
            users_collection.insert_one({'username': username, 'password': password})
            return redirect('/login')
        else:
            return "User already exists!"
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return "Login page - Add your login logic here"

if __name__ == '__main__':
    app.run()
