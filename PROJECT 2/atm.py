
import time

print("please insert your CARD")

time.sleep(5)

password = 1234

pin = int(input("Enter your atm pin"))

balance = 5000

while True:
    if pin==password:

        print('''
            1 == balance
            2 == withdraw balance 
            3 == deposit balance
            4 == exit''')

    try:
        option=int(input("Please enter your choice"))
    except:
        print("please enter the valid option")

    if option==1:
        print(f"your current balance is {balance}")
        print("===================================")
        print("===================================")
        print("===================================")

    if option==2:
            withdraw_amount=int(input("please enter withdrwa_amount"))
            print("===================================")
            print("===================================")

            balance = balance - withdraw_amount

            print(f"{withdraw_amount} is debited from your account")
            print(f"your updated balance is {balance}")

    if option==3:
            deposit_amount = int(input("please enter deposit_amount"))

            balance= balance + deposit_amount

            print(f"{deposit_amount} is debited from your account")
            print(f"your updated balance is {balance}")

    if option==4:
        break


else:
   print("Wrong pin please try again")

