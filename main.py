from tkinter import *
from app import AppTest
from pages.main_menu import MainMenu

if __name__ == '__main__':
    root = Tk()
    app = AppTest(root)
    app.show_page(MainMenu)
    root.mainloop()
 
