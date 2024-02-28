import tkinter as tk
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Application")
        self.geometry("640x480")

    def show_login_page(self):
        #show login page
        print("I am login page")

    def show_register_page(self):
        #show register page
        print("I am register page")
        
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
