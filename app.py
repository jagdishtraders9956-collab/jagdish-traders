from flask import Flask,render_template, request, redirect

import json

app = Flask(__name__)

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

@app.route("/admin", methods=["GET", "POST"])
def admin():
    brands = load_brands()

    if request.method == "POST":
        name = request.form["name"]
        image = request.form["image"]

        brands.append({"name": name, "image": image})
        save_brands(brands)

        return redirect("/admin")

    return render_template("admin.html", brands=brands)

@app.route("/delete/<int:index>")
def delete(index):
    brands = load_brands()
    brands.pop(index)
    save_brands(brands)
    return redirect("/admin")

if __name__ == "__main__":
    app.run()