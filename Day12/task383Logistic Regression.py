#Implement Logistic Regression on the Iris dataset. Evaluate model accuracy using .score().
# Import Libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Load Dataset
X, y = load_iris(return_X_y=True)

# Split Dataset (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Create Model
model = LogisticRegression(max_iter=200)

# Train Model
model.fit(X_train, y_train)

# Check Accuracy
accuracy = model.score(X_test, y_test)

print("Model Accuracy:", accuracy)


