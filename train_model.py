import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

data = pd.read_csv("plastic_data.csv")

features = [
    "bottles", "bags", "cups", "straws",
    "food_packages", "plates",
    "shopping_packages", "containers"
]

X = data[features]
y = data["plastic_kg"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("--------------------------------")
print("AI MODEL TRAINING")
print("--------------------------------")
print("Training completed successfully")
print("MAE:", round(mae, 2))
print("R2 Score:", round(r2, 2))

joblib.dump(model, "plastic_model.pkl")
print("Model saved as plastic_model.pkl")
print("--------------------------------")
