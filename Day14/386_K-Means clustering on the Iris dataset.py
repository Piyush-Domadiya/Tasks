#Implement K-Means clustering on the Iris dataset. Print out cluster labels.
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris

# Load dataset
iris = load_iris(as_frame=True)
X = iris.data.iloc[:, :2]
y = iris.target

# Train model
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)

# Cluster labels
labels = kmeans.labels_

print("Cluster Labels:", labels)    

# Visualize clusters
plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=labels, cmap='viridis')
plt.title("K-Means Clustering on Iris Dataset")
plt.xlabel("Sepal Length")
plt.ylabel("Sepal Width")
plt.show()