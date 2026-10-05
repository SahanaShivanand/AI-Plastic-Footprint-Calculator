from flask import Flask, render_template, request
import sqlite3
import joblib
from datetime import datetime

app = Flask(__name__)
model = joblib.load("plastic_model.pkl")

def create_database():
    conn = sqlite3.connect("database/plastic.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bottles INTEGER, bags INTEGER, cups INTEGER, straws INTEGER,
            food_packages INTEGER, plates INTEGER,
            shopping_packages INTEGER, containers INTEGER,
            monthly_kg REAL, yearly_kg REAL, category TEXT, date TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_category(kg):
    if kg < 1.5:
        return "LOW"
    elif kg <= 3:
        return "MEDIUM"
    return "HIGH"

def get_suggestions(data):
    suggestions = []
    if data["bottles"] >= 10:
        suggestions.append("Use a reusable water bottle.")
    if data["bags"] >= 10:
        suggestions.append("Use reusable shopping bags.")
    if data["cups"] >= 8:
        suggestions.append("Avoid single-use plastic cups.")
    if data["straws"] >= 5:
        suggestions.append("Avoid disposable plastic straws.")
    if data["food_packages"] >= 10:
        suggestions.append("Choose products with less plastic packaging.")
    if data["plates"] >= 5:
        suggestions.append("Use reusable plates.")
    if data["shopping_packages"] >= 8:
        suggestions.append("Reduce unnecessary online shopping packaging.")
    if data["containers"] >= 8:
        suggestions.append("Use reusable food containers.")
    if not suggestions:
        suggestions.append("Great! Your plastic usage is relatively low.")
    return suggestions

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    names = [
        "bottles", "bags", "cups", "straws",
        "food_packages", "plates",
        "shopping_packages", "containers"
    ]
    values = [int(request.form[name]) for name in names]

    input_data = [values]
    monthly_kg = float(model.predict(input_data)[0])
    yearly_kg = monthly_kg * 12
    category = get_category(monthly_kg)

    user_data = dict(zip(names, values))
    suggestions = get_suggestions(user_data)

    conn = sqlite3.connect("database/plastic.db")
    conn.execute("""
        INSERT INTO calculations (
            bottles, bags, cups, straws, food_packages, plates,
            shopping_packages, containers, monthly_kg, yearly_kg,
            category, date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (*values, monthly_kg, yearly_kg, category,
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    labels = [
        "Bottles", "Bags", "Cups", "Straws",
        "Food Packages", "Plates",
        "Shopping Packages", "Containers"
    ]

    return render_template(
        "result.html",
        monthly_kg=round(monthly_kg, 2),
        yearly_kg=round(yearly_kg, 2),
        category=category,
        suggestions=suggestions,
        labels=labels,
        values=values
    )

if __name__ == "__main__":
    create_database()
    app.run(debug=True)
