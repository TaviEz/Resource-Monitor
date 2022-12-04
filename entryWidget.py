#let the user decide what is the interval of measurement
import tkinter as tk

root = tk.Tk()
root.state("zoomed")

e = tk.Entry(root, width = 50,bg='blue', fg='white')
e.pack()
e.insert(0, "Enter your name: ")

text = tk.Text()
def myClick():
    myLabel = tk.Label(root, text=e.get())
    myLabel.pack()

btn1 = tk.Button(root, text='Save your name',padx=5,pady=5, command=myClick)
btn1.pack()

root.mainloop()