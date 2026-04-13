from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Replace this with your actual user loading logic
def load_users():
    return {} # Placeholder

def save_users(users):
    pass # Placeholder

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Your registration logic goes here
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
