#selection sort algorithm 
def selection_sort(arr):
    for i in range(len(arr)):
        min_index = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

data = list(map(int, input("Enter numbers you want to sort separated by spaces: ").split()))
print("Unsorted array:", data)
selection_sort(data)    
print("Sorted array:", data)