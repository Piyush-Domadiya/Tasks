#Reduce dimensions of the Iris dataset using PCA. Visualize the data in 2D using matplotlib.

import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

# Load Iris dataset
iris = load_iris(as_frame=True)
X = iris.data
y = iris.target

# Apply PCA (reduce to 2 dimensions)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# Print explained variance
print("Explained Variance Ratio:", pca.explained_variance_ratio_)

# Visualize in 2D
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis')
plt.title("PCA - 2D Visualization of Iris Dataset")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.colorbar(label="Species")
plt.show()
