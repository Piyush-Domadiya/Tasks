# import tkinter as tk

# # Create window
# root = tk.Tk()
# root.title("My First App")
# root.geometry("500x500")


# label = tk.Label(root, text="Hello Tkinter")
# label.pack()
 


# #run app
# root.mainloop()

import tkinter as tk

def show_text():
    print(entry.get())

root = tk.Tk()
root.geometry("500x500")
entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Submit", command=show_text)
button.pack()

root.mainloop()
