from flask import Flask, render_template, request, redirect, session
import json
from flask import send_from_directory

@app.route('/google12345abcd.html')
def google_verify():
    return send_from_directory('static', 'google12345abcd.html')

app = Flask(__name__)
app.secret_key = "jagdish_secret_key"   # important for login

USERNAME = "uttam"
PASSWORD = "uttam7905"

def load_brands():
    with open("brands.json", "r") as f:
        return json.load(f)

def save_brands(data):
    with open("brands.json", "w") as f:
        json.dump(data, f)

@app.route("/")
def home():
    brands = load_brands()
    return render_template("index.html", brands=brands)

# 🔐 LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user == USERNAME and pwd == PASSWORD:
            session["logged_in"] = True
            return redirect("/admin")
        else:
            return "Wrong username or password"

    return render_template("login.html")

# 🔐 ADMIN PANEL (PROTECTED)
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("logged_in"):
        return redirect("/login")

    brands = load_brands()

    if request.method == "POST":
        name = request.form["name"]
        image = request.form["image"]

        brands.append({"name": name, "image": image})
        save_brands(brands)

        return redirect("/admin")

    return render_template("admin.html", brands=brands)

# DELETE
@app.route("/delete/<int:index>")
def delete(index):
    if not session.get("logged_in"):
        return redirect("/login")

    brands = load_brands()
    brands.pop(index)
    save_brands(brands)
    return redirect("/admin")

# LOGOUT
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run()