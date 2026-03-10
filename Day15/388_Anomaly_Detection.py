# Implement Isolation Forest for anomaly detection
# Example: Detect outliers in the Iris dataset

# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# -------------------------------
# Step 1: Load the Iris dataset
# -------------------------------

# Load dataset as pandas DataFrame
iris = load_iris(as_frame=True)

# Extract feature matrix (only input features)
X = iris.data  

# Extract target labels (not used in anomaly detection)
y = iris.target

# Display first 5 rows of dataset
print("First 5 rows of dataset:")
print(X.head())


# -------------------------------
# Step 2: Feature Scaling
# -------------------------------

# Isolation Forest works better when data is scaled
scaler = StandardScaler()

# Transform features to mean=0 and std=1
X_scaled = scaler.fit_transform(X)


# -------------------------------
# Step 3: Apply Isolation Forest
# -------------------------------

# contamination=0.05 means we expect 5% data to be anomalies
model = IsolationForest(contamination=0.05, random_state=42)

# Train the model
model.fit(X_scaled)

# Predict anomalies
# Output:
#  1  -> Normal point
# -1  -> Anomaly (outlier)
predictions = model.predict(X_scaled)


# -------------------------------
# Step 4: Add predictions to dataset
# -------------------------------

# Add new column to original DataFrame
X['Anomaly'] = predictions

# Count number of normal and anomaly points
print("\nAnomaly Count:")
print(X['Anomaly'].value_counts())


# -------------------------------
# Step 5: Visualization (2D Plot)
# -------------------------------

# Create new figure
plt.figure()

# Plot normal points (prediction == 1)
plt.scatter(X_scaled[predictions == 1, 0],
            X_scaled[predictions == 1, 1],
            label="Normal")

# Plot anomaly points (prediction == -1)
plt.scatter(X_scaled[predictions == -1, 0],
            X_scaled[predictions == -1, 1],
            marker='x',
            label="Anomaly")

# Label axes
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")

# Show legend
plt.legend()

# Display plot
plt.show()