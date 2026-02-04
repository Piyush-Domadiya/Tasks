# Matrix Multiplication (Strassen's Algorithm)
import numpy as np

def next_power_of_2(n):
    power = 1
    while power < n:
        power *= 2
    return power

def pad_matrix(A, size):
    padded = np.zeros((size, size))
    padded[:A.shape[0], :A.shape[1]] = A
    return padded

def strassen(A, B):
    n = A.shape[0]

    # Base case
    if n == 1:
        return A * B

    mid = n // 2

    A11 = A[:mid, :mid]
    A12 = A[:mid, mid:]
    A21 = A[mid:, :mid]
    A22 = A[mid:, mid:]

    B11 = B[:mid, :mid]
    B12 = B[:mid, mid:]
    B21 = B[mid:, :mid]
    B22 = B[mid:, mid:]

    M1 = strassen(A11 + A22, B11 + B22)
    M2 = strassen(A21 + A22, B11)
    M3 = strassen(A11, B12 - B22)
    M4 = strassen(A22, B21 - B11)
    M5 = strassen(A11 + A12, B22)
    M6 = strassen(A21 - A11, B11 + B12)
    M7 = strassen(A12 - A22, B21 + B22)

    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    C = np.vstack((
        np.hstack((C11, C12)),
        np.hstack((C21, C22))
    ))

    return C

import numpy as np

n = int(input("Enter size of matrix: "))

A = np.random.randint(1, 10, size=(n, n))
B = np.random.randint(1, 10, size=(n, n))

# Padding if needed
m = next_power_of_2(n)
A_pad = pad_matrix(A, m)
B_pad = pad_matrix(B, m)

# Strassen multiplication
C_pad = strassen(A_pad, B_pad)

# Remove padding
C = C_pad[:n, :n]

print("Matrix A:\n", A)
print("Matrix B:\n", B)
print("Result:\n", C)
