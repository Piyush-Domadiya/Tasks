# Build a Simple Neural Network using Keras
# Example: Classify the Iris dataset

# Import required libraries
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

# ----------------------------
# Step 1: Load Dataset
# ----------------------------

iris = load_iris()
X = iris.data          # Features (4 input features)
y = iris.target        # Target labels (0,1,2)

# ----------------------------
# Step 2: One-Hot Encoding
# ----------------------------
# Convert labels into categorical format for multi-class classification
y = to_categorical(y)

# ----------------------------
# Step 3: Train-Test Split
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# ----------------------------
# Step 4: Feature Scaling
# ----------------------------

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ----------------------------
# Step 5: Build Neural Network
# ----------------------------

model = Sequential()

# Hidden Layer 1
model.add(Dense(16, activation='relu', input_shape=(4,)))

# Hidden Layer 2
model.add(Dense(8, activation='relu'))

# Output Layer (3 classes)
model.add(Dense(3, activation='softmax'))

# ----------------------------
# Step 6: Compile Model
# ----------------------------

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ----------------------------
# Step 7: Train Model
# ----------------------------

model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=8,
    validation_split=0.1
)


# ----------------------------
# Step 8: Evaluate Model
# ----------------------------

loss, accuracy = model.evaluate(X_test, y_test)


train_loss, train_accuracy = model.evaluate(X_train, y_train)
print("Train Accuracy:", train_accuracy)
# ----------------------------
print("Test Accuracy:", accuracy)