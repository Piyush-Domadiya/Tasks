import streamlit as st
import numpy as np
import cv2
import os

from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping

from streamlit_drawable_canvas import st_canvas


st.title("Handwritten Digit Recognition with Self Learning")

MODEL_PATH = "mnist_cnn_model.keras"
DATASET_PATH = "feedback_data"


# --------------------------
# Create dataset folders
# --------------------------

for i in range(10):
    os.makedirs(f"{DATASET_PATH}/{i}", exist_ok=True)


# --------------------------
# Build CNN Model
# --------------------------

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


# --------------------------
# TRAIN MODEL BUTTON
# --------------------------

if st.button("Train Model"):

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

    st.success(f"Model trained! Accuracy: {acc:.4f}")


# --------------------------
# LOAD MODEL
# --------------------------

if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
else:
    st.warning("Please train the model first.")
    st.stop()


# --------------------------
# DRAW DIGIT
# --------------------------

st.subheader("Draw a Digit")

canvas = st_canvas(
    fill_color="white",
    stroke_width=15,
    stroke_color="black",
    background_color="white",
    height=280,
    width=280,
    drawing_mode="freedraw",
    key="canvas",
)


# --------------------------
# PREDICT DIGIT
# --------------------------

if st.button("Predict"):

    if canvas.image_data is not None:

        img = canvas.image_data[:,:,0]

        img = cv2.resize(img,(28,28))

        img = img/255.0

        img = img.reshape(1,28,28,1)

        pred = model.predict(img)

        digit = np.argmax(pred)

        st.success(f"Predicted Digit: {digit}")

        st.session_state["image"] = img


# --------------------------
# FEEDBACK SECTION
# --------------------------

if "image" in st.session_state:

    correct_digit = st.number_input(
        "Enter correct digit if prediction was wrong",
        0,9
    )

    if st.button("Save Image"):

        img = st.session_state["image"]

        img_save = (img.reshape(28,28)*255).astype("uint8")

        folder = f"{DATASET_PATH}/{correct_digit}"

        count = len(os.listdir(folder))

        path = f"{folder}/{count}.png"

        cv2.imwrite(path,img_save)

        st.success("Image saved for learning!")


# --------------------------
# TRAIN USING FEEDBACK DATA
# --------------------------

if st.button("Learn From Saved Images"):

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

    if len(images) == 0:

        st.warning("No saved images found")

    else:

        X = np.array(images).reshape(-1,28,28,1)

        y = to_categorical(labels,10)

        model.fit(X,y,epochs=3)

        model.save(MODEL_PATH)

        st.success("Model learned from saved images!")