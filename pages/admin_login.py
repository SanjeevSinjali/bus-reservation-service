# login_page.py
import tkinter as tk
from tkinter import ttk,messagebox
from lib import globals
class LoginPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Login Page")
        self.master.geometry("750x700")
        self.master.resizable(False, False)

        img_label = tk.Label(self.master)
        img_label.place(relx=0, rely=0, relwidth=0.5, relheight=1)
        img = tk.PhotoImage(file="/Users/sanjeev/Desktop/bus-reservation-service/data/images/bus.png")
        img_label.config(image=img)
        img_label.image = img

        self.login_frame = tk.Frame(self.master)
        self.login_frame.place(relx=0.5, rely=0.4, relwidth=0.5, relheight=0.4)

        self.loginPage()

    def loginPage(self):

        welcome_lbl = ttk.Label(self.login_frame,text="Welcome Back!")
        welcome_lbl.grid(row=0, column=0,padx=0, pady=10, sticky="e")

        self.default_username = tk.StringVar()
        self.default_password = tk.StringVar()

        lbl_username = ttk.Label(self.login_frame, text="Username:")
        lbl_username.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.entry_username = ttk.Entry(self.login_frame, textvariable=self.default_username)
        self.entry_username.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        lbl_password = ttk.Label(self.login_frame, text="Password:")
        lbl_password.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.entry_password = ttk.Entry(self.login_frame, textvariable=self.default_password, show="*")
        self.entry_password.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        btn_login = ttk.Button(self.login_frame, text="Login", command=self.login)
        btn_login.grid(row=3, column=1, padx=10, pady=0, sticky="e")

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        print("Username:", username)
        print("Password:", password)

    def createAccount(self):
        self.destroy()
        #Go to signup page