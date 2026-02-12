import tensorflow as tf
import numpy as np

# Data
X = np.array([1,2,3,4,5], dtype=float)
y = np.array([2,4,6,8,10], dtype=float)

# Create Model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(1, input_shape=[1])
])

# Compile
model.compile(optimizer='sgd', loss='mean_squared_error')

# Train
model.fit(X, y, epochs=500, verbose=0)

# Predict
print(model.predict([6.0]))
