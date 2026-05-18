# Rearrange the array such that the first half of the array is in increasing order and the second half is in decreasing order.  

# def arrage(arr):
#     arr.sort()

#     n = len(arr)
#     # arr[n//2:] = reversed(arr[n//2:])
#     arr[n//2:] = arr[n//2:][::-1]
#     return arr


# num =int(input("Enter the number of elements in the array: "))
# arr = list(map(int, input("Enter elements: ").split()))
# arrage(arr)
# print(arr)



# SUm and avg of array elements

# def total(arr):
#     total = 0.0

#     # for i in arr:
#     #     total += i
# # OR 
#     for i in range(len(arr)):
#         total += arr[i]

#     avg = total / len(arr)
#     print(f"Average: {avg}")

#     return total
    
# num = int(input("Enter the number of elements in the array: "))
# arr = list(map(int, input("Enter elements: ").split()))         
# result = total(arr)
# print(result)