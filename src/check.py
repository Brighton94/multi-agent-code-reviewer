import tkinter as tk
from tkinter import messagebox

def on_button_click():
    messagebox.showinfo("Success", "Button was clicked!")

root = tk.Tk()
root.title("Test Window")

button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack(pady=20)

root.mainloop()