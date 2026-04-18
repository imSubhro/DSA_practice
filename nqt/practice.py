# prime Number
# num = int(input("Enter a number: "))

# if num <= 1:
#     print("Not prime")
# else:
#     for i in range (2,num):
#         if num%i ==0 :
#             print("Not prime")
#             break
#     else:        
#         print("Prime Number")


#palindrome Number
# num = int(input("Enter a number: "))

# temp =num
# rev = 0 

# while temp > 0:
#     digit = temp % 10
#     rev = rev *10 + digit 
#     temp = temp // 10

# if num == rev:
#     print("Palindrome Number")
# else:
#     print("Not a Palindrome Number")


#reverse number

# num = int(input("Enter a number: "))

# temp = num 
# rev= 0

# while temp>0:
#     digit = temp%10
#     rev = rev*10 +digit
#     temp = temp //10
# print("Reverse of", num, "is: ", rev)

#fibonacci Series
# num = int(input("Enter number: "))

# a=0
# b=1

# print("Fibonacci Series: ", end=" ")

# for i in range(num):
#     print(a, end=" ")
#     c= a+b
#     a=b
#     b=c


# #factorial of a number

# num = int(input("Enter a number: "))

# fact = 1

# for i in range (1, num+1):
#     fact = fact * i

# print("Factorial of", num, "is: ", fact)


#  Armstrong Number

# num = int(input("Enter a number: "))

# temp = num 
# sum = 0
# while temp > 0:
#     digit = temp % 10
#     sum = sum + digit ** 3
#     temp = temp // 10

# if num == sum:
#     print(num, "is an Armstrong Number")
# else:   print(num, "is not an Armstrong Number")        


#leap Year

# num = int(input("Enter a year: "))

# if (num%4 ==0 and num%100 !=0) or (num%400 ==0):
#     print(num, "is a leap year")
# else:
#     print(num, "is not a leap year")


#lcm check

# num1 = int(input("Enter first number: "))
# num2 = int(input("Enter second number: "))

# max_num = max(num1, num2)

# while True:
#     if max_num % num1 == 0 and max_num % num2 == 0:
#         print("LCM of", num1, "and", num2, "is: ", max_num)
#         break
#     max_num += 1

#gcd/hcf check

# num1 = int(input("Enter first number: "))
# num2 = int(input("Enter second number: "))

# if num2 != 0:
#     num1, num2 = num2, num1 % num2
# print("GCD/HCF of the two numbers is: ", num1)


# Array input

# n = int(input("Enter the size of the array: "))
# arr = list(map (int, input("Enter the elements of the array: ").split()))

#REVERSE ARRAY
# print("reversed array: ", arr[::-1])

# #SUM OF ARRAY
# total = 0
# for num in arr:
#     total += num
# print("Sum of elements in the array: ", total)

#sorted array
# sorted_arr = sorted(arr)
# print("Sorted array: ", sorted_arr)

# is_sorted = True

# for i in range(len(arr) - 1):
#     if arr[i] > arr[i + 1]:
#         is_sorted = False
#         break

# if is_sorted:
#     print("Sorted")
# else:
#     print("Not Sorted")