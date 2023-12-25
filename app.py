import json
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'Binale'  # Set a secret key for session security
MY_DATA = 'users.txt'

def load_data():
    with open(MY_DATA, 'r') as filehandle:
        return json.load(filehandle)

def save_to_file(users):
    with open(MY_DATA, 'w') as filehandle:
        json.dump(users, filehandle)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        users = load_data()
        for usr in users:
            if user == usr["name"] and pwd == usr["pwd"]:
                session['user'] = user  # Store user in session
                return redirect(url_for('success'))
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        users = load_data()
        users.append({"name": user, "pwd": pwd})
        save_to_file(users)
        session['user'] = user  # Store user in session
        return redirect(url_for('success'))
    return render_template("signup.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/success")
def success():
    user = session.get('user')
    if user:
        return render_template("success.html", user=user)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
