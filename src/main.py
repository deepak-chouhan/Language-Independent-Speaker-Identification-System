import os
import tkinter as tk
import speech_recognition as sr


def myAction():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listinig....")
            audio = r.listen(source)
        try:
            text = (r.recognize_google(audio), "\n")
        except:
            pass


window = tk.Tk()
window.title("Speaker identification system")
window.minsize(width=500, height=500)

button = tk.Button(text="Okay", command=myAction)
button.pack()

window.mainloop()
