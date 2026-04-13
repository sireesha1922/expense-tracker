import os
import urllib.parse
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Safely hard-coded credentials to avoid "Invalid URI" errors
username = urllib.parse.quote_plus("sireeshaerikela_db_user")
password = urllib.parse.quote_plus("Siri@123$")
cluster_url = "cluster0.ms3havz.mongodb.net"

# Construct the URI
mongo_uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)
db = client['expense_db']
users_collection = db['users']

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not users_collection.find_one({'username': username}):
            users_collection.insert_one({'username': username, 'password': password})
            return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return "Login page active"

if __name__ == '__main__':
    app.run()
