# Implement a Decision Tree Classifier. Example: Apply it on the Iris dataset.

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Load dataset
iris = load_iris(as_frame=True)
X = iris.data
y = iris.target

# Train model
model = DecisionTreeClassifier(max_depth=4, random_state=42)
model.fit(X, y)

# Accuracy
y_pred = model.predict(X)
print("Accuracy:", accuracy_score(y, y_pred))

# Plot tree
plt.figure(figsize=(12,8))
plot_tree(model,
          feature_names=iris.feature_names,
          class_names=iris.target_names,
          filled=True)

plt.show()
