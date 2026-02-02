# Bubble Sort Algorithm
def bubble_sort(arr):
    n=len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j]>arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

data = list(map(int, input("Enter numbers you want to sort separated by spaces: ").split()))
print("Unsorted array:", data)
bubble_sort(data)   
print("Sorted array:", data)