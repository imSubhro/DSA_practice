import random

# snake water gun or Rock paper scissors

def game(comp, you):
# If two values are equal , declare a tie!
    if comp == you:
        return None

 #  Check for all possibilites when computer chose s

    if comp =='s':
        if you== 'w':
            return False
        elif you== 'g':
                return True
#  Check for all possibilites when computer chose w
        elif comp == 'w':
                    if you == 'g':
                        return False
                    elif you == 's':
                            return True
 #  Check for all possibilites when computer chose g
                    elif comp == 'g':
                     if you == 's':
                        return False
                    elif you == 'w':
                            return True

a = print("Comp Turn: Snake(s) Water(w) or Gun(g)?")
randNo = random.randint(1,3)
print(randNo)
if randNo == 1:
    comp ='s'
elif randNo == 2:
    comp = 'w'
elif randNo == 3:
    comp ='g'

b = input("Your Turn: Snake(s) Water(w) or Gun(g)?")

game(comp, 'you')

print(f"Computer chose {comp}")
print(f"You chose you")

if a == None:
    print("The game is a tie!")
elif a:
     print("You Win!")
else:
     print("You Lose!")
