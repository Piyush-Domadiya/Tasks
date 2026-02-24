# Implement KNN classifier on the Iris dataset. Evaluate accuracy using .score().

from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
iris = load_iris(as_frame=True)
X = iris.data
y = iris.target

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train KNN model
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# Evaluate model accuracy
y_pred = knn.predict(X_test)
accuracy = knn.score(X_test, y_test)

print("Predicted labels:", y_pred)
print("KNN Model Accuracy:", accuracy)