import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

#Sample data
data = np.array([10,12,13,15,18,20,21,23,25,28,30,32,35,37,40]).reshape(-1,1)

#Normalize the data
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

#Create sequences
X = []
y = []
window = 3

for i in range(len(data_scaled)-window):
    X.append(data_scaled[i:i+window])
    y.append(data_scaled[i+window])

X = np.array(X)
y = np.array(y)


#Train-Test Split
split = int(len(X)*0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

#Build LSTM Model
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(window,1)))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=300, verbose=0)

#Predict and evaluate
pred = model.predict(X_test)

predicted = scaler.inverse_transform(pred)
actual = scaler.inverse_transform(y_test)


#Evaluate 
rmse = np.sqrt(mean_squared_error(actual, predicted))
print("RMSE:", rmse)

#Plotting
plt.plot(actual, label="Actual")
plt.plot(predicted, label="Predicted")
plt.legend()
plt.show()