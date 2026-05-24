# def palindrome(n):
#     s = str(n)
#     return s == s[::-1] 

# # Driver code   
# n = 12321
# if palindrome(n):
#     print("Yes")
# else:
#     print("No")


# Function to check if a number is a palindrome into a given range
def palindrome(n):

    revnum = 0
    temp = n

    while n >0:
        id = n%10
        revnum = revnum*10 + id
        n = n//10

    return revnum == temp

min = int(input("Enter the minimum range: "))
max = int(input("Enter the maximum range: "))

for i in range (min,max+1):
    if palindrome(i):
        print(i,end=" ")

