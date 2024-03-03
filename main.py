import tkinter as tk
import os
from pages import cus_login,cus_register
from lib import globals
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bus Reservation Service")
        self.geometry("640x480")
        self.show_login_page()


    def show_login_page(self):
        self.login_page = cus_login.LoginPage(self)
        self.login_page.pack(fill="both", expand=True)

    def show_register_page(self):
        self.register_page = cus_register.RegisterPage(self)
        
if __name__ == "__main__":
    globals.dataPath = os.path.abspath("./data/images")
    app = MainApp()
    app.mainloop()
