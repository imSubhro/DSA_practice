# # Solution class containing removeDuplicates method
# class Solution:
#     # Removes duplicates using set and returns count of unique elements
#     def removeDuplicates(self, nums):
#         # Set to store seen unique elements
#         seen = set()

#         # Position to overwrite next unique element
#         index = 0

#         # Iterate over each number in nums
#         for num in nums:
#             # If num is not in seen, it is unique
#             if num not in seen:
#                 # Add num to set
#                 seen.add(num)

#                 # Overwrite nums[index] with this num
#                 nums[index] = num

#                 # Move index forward
#                 index += 1

#         # Return number of unique elements
#         return index


# # Driver code
# nums = [0,0,1,1,1,2,2,3,3,4]
# sol = Solution()
# k = sol.removeDuplicates(nums)

# print("k =", k)
# print("Array after removing duplicates:", nums[:k])



## Remove duplicates from sorted array without using extra space
# def removeDuplicates(arr):
#     if len(arr) == 0:
#         return 0
    
#     i =0
#     for j in range (1,len(arr)):
#         if arr[i] != arr[j]:
#             i+=1
#             arr[i] = arr[j]

#     return i+1

# # Driver code
# nums = [0,0,1,1,1,2,2,3,3,4,5,5,6,7,7,8,9,9]
# k = removeDuplicates(nums)

# print("k =", k)
# print("Array after removing duplicates:", nums[:k])



## Remove deplicates form unsorted array 

def removeDuplicates(arr):
    
    result =[]

    for i in range(len(arr)):
        found = False

        for j in range(len(result)):
            if arr[i] == result[j]:
                found = True
                break

        if not found:
            result.append(arr[i])

    return result

# Driver code
nums = [3, 1, 2, 3, 4, 1, 5, 2, 6, 7, 8, 9, 9]
unique_nums = removeDuplicates(nums)    
print("Array after removing duplicates:", unique_nums)  
