from tkinter import *
root = Tk()
root.title("Overlay Example")
x="0"
y="0"
root.geometry(f"300x200+{x}+{y}")
root.overrideredirect(True)  # Remove window decorations
root.attributes("-transparentcolor", "red")  # Set transparency
root.config(bg="red")  # Set background color to match transparency

# Create a label with text
l=Label(root, text="Overlay Text", bg="red", fg="white", font=(60))
l.pack()

# Create a canvas for drawing
canvas = Canvas(root, width=300, height=200, bg="red", highlightthickness=0)
canvas.pack()

# Create a rectangle on the canvas
rectangle = canvas.create_rectangle(50, 50, 250, 150, fill="red", outline="blue")

root.wm_attributes("-topmost", 1)  # Keep the window on top
root.mainloop()
