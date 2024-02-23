import tkinter as tk
from tkinter import PhotoImage

def let_go():
    print("Let's Go!")

root = tk.Tk()
root.title("Background Image Example")

# Load the background image
bg_image = PhotoImage("Scooter.jpg")

# Create a label to display the background image
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)  # Cover the entire window

# Create a button
button = tk.Button(root, text="Let Go", command=let_go, font=("Arial", 16))
button.pack(pady=20)

root.mainloop()