import tkinter as tk
from pages import cus_login
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Application")
        self.geometry("640x480")
        self.show_login_page()


    def show_login_page(self):
        self.login_page = cus_login.LoginPage(self)
        self.login_page.pack(fill="both", expand=True)
        #show login page
        print("I am login page")

    def show_register_page(self):
        #show register page
        print("I am register page")
        
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
