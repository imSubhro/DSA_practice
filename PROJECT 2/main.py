import random
randNumber = random.randint(1,100)
print(randNumber)
usarGuess = None
guesses = 0

while(usarGuess != randNumber):
    usarGuess = int(input("Enter your guess:"))
    guesses +=1
    if(usarGuess== randNumber):
        print("You guessed it right!")
    else:
        if(usarGuess>randNumber):
            print("You guessed it wrong! Enter a smaller number")
        else:
            print("You guessed it wrong! Enter a larger number")

print(f"You gueesed the number in {guesses} guesses ")
with open("hiscore.txt", "r")as f:
    hiscore = int(f.read())

if (guesses<hiscore):
    print("You have just broken the high scorer!")
    with open("hiscore.txt", "w") as f:
        f.write(guesses)
        
 