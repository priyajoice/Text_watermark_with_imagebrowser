from tkinter import *
from PIL import Image, ImageTk


class SlideShowGUI:

    def __init__(self, img_lt, counter=0):
        self.root = Tk()
        self.root.title("Watermarked Image")
        self.counter = counter
        self.images_list = img_lt

        self.photo = self.open_image(self.counter)

        self.b1 = Button(self.root, text="", image=self.photo, bg="white")
        self.b1.pack()

        back = Button(self.root, anchor=W, text="Previous", relief=RIDGE, command=self.previous_image)
        back.pack(side=LEFT, padx=100, pady=20)

        forward = Button(self.root, anchor=E, text="Next", relief=RIDGE, command=self.next_image)
        forward.pack(side=RIGHT, padx=100, pady=20)

        self.root.mainloop()

    def open_image(self, counter):
        img = Image.open(self.images_list[counter])
        img = img.resize((500, 500), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        return photo

    def previous_image(self):
        self.counter -= 1
        try:
            self.photo = self.open_image(self.counter)
            self.b1.configure(image=self.photo)
        except IndexError:
            self.counter = 0
            self.previous_image()

    def next_image(self):
        self.counter += 1
        try:
            self.photo = self.open_image(self.counter)
            self.b1.configure(image=self.photo)
        except IndexError:
            self.counter = -1
            self.next_image()








