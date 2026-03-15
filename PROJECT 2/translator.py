from googletrans import Translator
user = input("enter text to translate")
Translator = Translator()
a= Translator.translate(user, src="en",dest= "bn")
print(a.text)
