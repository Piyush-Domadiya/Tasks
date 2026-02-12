""" NumPy can handle large data efficiently because:
✔ Continuous memory allocation
✔ Same data type (less overhead)
✔ Vectorized operations (no Python loops)
✔ C-level optimization
✔ Fast mathematical functions """

import numpy as np

arr = np.array([[1,2,3,4,5],[3,4,5,4,5]])
arr1= np.array([[2,3],[4,5],[6,7],[7,8],[8,9]])
print(arr)
print("Shape of the array:", arr.shape)

# Mathematical Operations
print("Addition arr+5:", arr + 5)
print("Multiplication arr*3:", arr * 3)

#Statistical Operations
print("Mean of the array:", arr.mean())
print("Standard Deviation of the array:", arr.std())
print("maximum value in the array:", arr.max())

print(arr.dot(arr1))       # Matrix multiplication
print(np.transpose(arr)) # Transpose