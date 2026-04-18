##Linear Search

# def linear_search(arr, target):
#     for i in range(len(arr)):
#         if arr[i] == target:
#             return f"Found at index {i}"
#     return "Element not found"

# n= int(input("Enter the number of elements in the array: "))
# arr = list(map(int, input("Enter the elements of the array: ").split()))
# target = int(input("Enter the target element to search: "))

# result = linear_search(arr,target)

# print(result)


#Binary Search

def binary_search(arr,target):
    low=0
    high=len(arr)-1
    while low<=high:
        mid = (high+low)//2
        if arr[mid] == target:
            return f"Found at index {mid}"
        elif arr[mid]<target:
            low = mid+1
        else:
            high = mid-1
    return "Element not found"

n= int(input("Enter the number of elements in the array: "))
arr = list(map(int, input("Enter the elements of the array: ").split()))
# arr.sort() # Binary search requires the array to be sorted
target = int(input("Enter the target element to search: "))
result = binary_search(arr,target)
print(result)