import os
import urllib.parse
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Safely encode the password to handle special characters like '@' and '$'
username = urllib.parse.quote_plus("sireeshaerikela_db_user")
password = urllib.parse.quote_plus("Siri@123$")
cluster_url = "cluster0.ms3havz.mongodb.net"

# Construct the full connection string
mongo_uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"

# Initialize MongoDB
client = MongoClient(mongo_uri)
db = client['expense_db']
users_collection = db['users']

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if user already exists
        if users_collection.find_one({'username': username}):
            return "User already exists! Try a different username."
            
        # Insert user into MongoDB
        users_collection.insert_one({'username': username, 'password': password})
        return redirect('/login')
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Find user in MongoDB
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            return "Login Successful!"
        else:
            return "Invalid username or password."
            
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
