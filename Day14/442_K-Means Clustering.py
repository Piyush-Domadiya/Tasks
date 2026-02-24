#Implementation of K-Means Clustering

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Sample 2D data
X = np.array([
    [1, 1],
    [1.5, 2],
    [2, 3],
    [3, 4],
    [5, 7],
    [3.5, 5],
    [4.5, 5],
    [3.5, 4.5]
])


kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)

# Cluster labels
labels = kmeans.labels_

# Centroids
centroids = kmeans.cluster_centers_

print("Cluster Labels:", labels)
print("Centroids:\n", centroids)

plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
plt.scatter(centroids[:, 0], centroids[:, 1], 
            marker='X', s=200)

plt.title("K-Means Clustering")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()

