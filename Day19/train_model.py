import numpy as np
import os
import cv2

from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping


MODEL_PATH = "mnist_cnn_model.keras"
DATASET_PATH = "feedback_data"


# -----------------------------
# create folders
# -----------------------------
for i in range(10):
    os.makedirs(f"{DATASET_PATH}/{i}", exist_ok=True)


# -----------------------------
# build CNN
# -----------------------------
def build_model():

    inputs = Input(shape=(28,28,1))

    x = Conv2D(32,(3,3),activation="relu")(inputs)
    x = BatchNormalization()(x)
    x = MaxPooling2D(2,2)(x)

    x = Conv2D(64,(3,3),activation="relu")(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D(2,2)(x)

    x = Flatten()(x)

    x = Dense(128,activation="relu")(x)

    x = Dropout(0.3)(x)

    outputs = Dense(10,activation="softmax")(x)

    model = Model(inputs,outputs)

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


# -----------------------------
# TRAIN MODEL
# -----------------------------
print("Loading MNIST dataset...")

(X_train,y_train),(X_test,y_test) = mnist.load_data()

X_train = X_train/255.0
X_test = X_test/255.0

X_train = X_train.reshape(-1,28,28,1)
X_test = X_test.reshape(-1,28,28,1)

y_train = to_categorical(y_train,10)
y_test = to_categorical(y_test,10)

model = build_model()

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=3,
    restore_best_weights=True
)

print("Training model...")

model.fit(
    X_train,
    y_train,
    validation_split=0.2,
    epochs=5,
    batch_size=64,
    callbacks=[early_stop]
)

model.save(MODEL_PATH)

loss,acc = model.evaluate(X_test,y_test)

print("Model trained!")
print("Accuracy:",acc)


# -----------------------------
# LEARN FROM FEEDBACK IMAGES
# -----------------------------
print("Checking feedback images...")

images = []
labels = []

for digit in range(10):

    folder = f"{DATASET_PATH}/{digit}"

    for file in os.listdir(folder):

        img = cv2.imread(f"{folder}/{file}",0)

        img = cv2.resize(img,(28,28))

        img = img/255.0

        images.append(img)

        labels.append(digit)


if len(images) > 0:

    print("Learning from saved images...")

    X = np.array(images).reshape(-1,28,28,1)

    y = to_categorical(labels,10)

    model = load_model(MODEL_PATH)

    model.fit(X,y,epochs=3)

    model.save(MODEL_PATH)

    print("Model updated with feedback images!")

else:

    print("No feedback images found.")