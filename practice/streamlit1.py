import streamlit as st
import numpy as np

st.title("Simple Prediction App")

number = st.number_input("Enter a number")

result = number * 2

st.write("Result:", result)
