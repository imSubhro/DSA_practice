# def countfreq(arr):

#     freq = {}
#     for num in arr:
#         if num in freq:
#             freq[num] += 1
#         else:
#             freq[num] = 1


#     # return freq
#     for key, value in freq.items():
#         print(f"{key}: {value}")

# n = int(input("Enter the number of elements in the array: "))
# arr = list(map(int, input("Enter the elements of the array: ").split()))
# result = countfreq(arr)
# print(result)


# Alternative approach using visited array
# def countfreq(arr,n):
#     visited = [False] * n

#     for i in range(n):
#         if visited[i]:
#             continue

#         count = 1
#         for j in range(i+1, n):
#             if arr[i] == arr[j]:
#                 visited[j] = True
#                 count += 1

#         print(f"{arr[i]}: {count}")

# if __name__ == "__main__":
#     # Input array
#     arr = [10, 5, 10, 15, 10, 5]
#     n = len(arr)

#     # Call the function to count frequencies
#     countfreq(arr, n)