
from datetime import date


letter = '''Dear <|Name|>,
Greetings from ABC coding house. I am happy to tell you about your selection
You are selected!
Have a great day ahead!
Thanks and regards,
Bill
Date: <|DATE|>
'''
name = input("Enter Your name\n")
name = input("Enter Date\n")
letter =letter.replace("<|NAME|>", name)
letter = letter.replace("<|DATE|>", date)
print(letter)



