from tkinter import *
from textblob import TextBlob


def check_spelling():
    a= TextBlob(spell_check.get())
    spell= Label(window,text="Rectified:", font=("arial",15,"bold"), bg="gray")
    spell.pack()
    correct_text= Label(window, text=str(a.correct()),font=("Arial",20,"bold"),bg="pink")
    correct_text.pack()


window = Tk()
window.title("Nomadic Spell Checker ")
window.geometry("800x600")
window.config(background ="seagreen")

text_heading=Label(window,text="Spelling Checker",font=("calibri",50,"bold"),bg="indigo",fg="magenta")
text_heading.pack()

text_check= Label(window, text="Enter your spelling", font=("ariel", 30,"bold"), bg="crimson",fg="black" )
text_check.pack()

spell_check= Entry(window, font=("Calibri",15,"bold"),width="400",bg="lightblue")
spell_check.pack()


Check_button = Button(window, text="Check!!", font=("Arial",20,"bold"),fg="white", bg= "red",command=check_spelling)
Check_button.pack()

text_wmk= Label(window, text="Nomad",font= ("futura",10,"bold"),bg="green")
text_wmk.pack()

window,mainloop()
