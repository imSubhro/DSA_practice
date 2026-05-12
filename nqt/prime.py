##normal prime number program

# num = int(input("Enter a number: "))

# if num >1 :
#     is_prime = True

# for i in range(2,num):
#     if num%i == 0:
#         is_prime = False
#         break
    
#     if is_prime:
#         print(f"{num} is a prime number")   
#     else:   
#         print(f"{num} is not a prime number")

# else:
#     print(f"{num} is not a prime number")



## prime numbr for a given range 

# start = int(input("Enter the starting number: "))
# end = int(input("Enter the ending number: "))

# for num in range (start,end+1):
#     if num>1:
        
#         for i in range(2,num):
#             if num%i == 0:
#                 is_prime = False
#                 break 
#         else:
#             print(num)
        


# prime number given 1 gap prime no 

# start = int(input("Enter the starting number: "))
# end = int(input("Enter the ending number: "))   
# gap = int(input("Enter the gap between prime numbers: "))

# primes =[]

# for num in range (start,end+1):
#     if num>1:
#         is_prime = True
#         for i in range(2,num):
#             if num%i == 0:
#                 is_prime = False
#                 break 
#         else:
#             primes.append(num)

        
# for i in range(0, len(primes), gap+1):
#     print(primes[i], end=" ")

        