import os
from flask import Flask, request, render_template, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB using the URI we saved in Render
client = MongoClient(os.environ.get('MONGO_URI'))
db = client['expense_db'] # Your database name
users_collection = db['users']

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user already exists
        if users_collection.find_one({'username': username}):
            return "User already exists!"
            
        # Save to MongoDB
        users_collection.insert_one({'username': username, 'password': password})
        return redirect('/login')
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Similar logic for login using users_collection.find_one({'username': username})
    return "Login page"

if __name__ == '__main__':
    app.run(debug=True)
