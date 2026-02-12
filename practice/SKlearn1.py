import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
# Input (Experience)
X = np.array([[1], [2], [3], [4], [5]])

# Output (Salary)
y = np.array([20000, 30000, 40000, 50000, 60000])

# Create Model
model = LinearRegression()

# Train Model
model.fit(X, y)
# Predict
prediction = model.predict([[6]]) # type: ignore
print("Predicted Salary:", prediction)


joblib.dump(model, "model.pkl", compress=9)
# Load Model
loaded_model = joblib.load("model.pkl")

# Predict
print(loaded_model.predict([[7]]))