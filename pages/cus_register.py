import tkinter as tk
from tkinter import ttk,messagebox
import re
from pages import cus_login
from lib import globals
from lib import dbfunctions

class RegisterPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.db_instance = dbfunctions.dbfunctions()
        self.master.title("Register Page")
        self.master.geometry("750x700")
        self.master.resizable(False, False)
        self.Page()

    def Page(self):
        img_label = tk.Label(self.master)
        img_label.place(relx=0, rely=0, relwidth=0.5, relheight=1)
        img = tk.PhotoImage(file=globals.dataPath+"/bus.png")
        img_label.config(image=img)
        img_label.image = img

        register_frame = tk.Frame(self.master)
        register_frame.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.8)

        register_lbl = ttk.Label(register_frame,text="Register")
        register_lbl.grid(row=0, column=1,padx=0, pady=10, sticky="e")
        
        ttk.Label(register_frame, text="Full Name:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_fullname = ttk.Entry(register_frame)
        self.entry_fullname.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(register_frame, text="Email:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_email = ttk.Entry(register_frame)
        self.entry_email.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(register_frame, text="Phone Number:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.entry_phone = ttk.Entry(register_frame)
        self.entry_phone.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(register_frame, text="Password:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.entry_password = ttk.Entry(register_frame, show="*")
        self.entry_password.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(register_frame, text="Re-enter Password:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.entry_repassword = ttk.Entry(register_frame, show="*")
        self.entry_repassword.grid(row=5, column=1, padx=10, pady=10, sticky="w")
                
        ttk.Label(register_frame, text="Recovery Passphrase:").grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.entry_recover_passphrase = ttk.Entry(register_frame)
        self.entry_recover_passphrase.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(register_frame, text="Pin:").grid(row=7, column=0, padx=10, pady=10, sticky="e")
        self.pin_user = ttk.Entry(register_frame)
        self.pin_user.grid(row=7, column=1, padx=10, pady=10, sticky="w")


        ttk.Button(register_frame, text="Register", command=self.register).grid(row=8, column=1, padx=10, pady=10, sticky="e")

    def register(self):
        fullname = self.entry_fullname.get()
        email = self.entry_email.get()
        phone = self.entry_phone.get()
        password = self.entry_password.get()
        repassword = self.entry_repassword.get()
        recover_phrase = self.entry_recover_passphrase.get()
        pin = self.pin_user.get()

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(email_pattern, email):
            tk.messagebox.showerror(title="Error",message="Email is not correct")
            print("Invalid email address")
            return

        if password != repassword:
            tk.messagebox.showerror(title="Error",message="Password did not match")
            return
        
        if pin is None:
            tk.messagebox.showerror(title="Error",message="Pin must be entered")
            return

        print("Full Name:", fullname)
        print("Email:", email)
        print("Phone Number:", phone)
        print("Password:", password)
        print("Re-entered Password:", repassword)

        user = self.db_instance.create_user(fullname,password,email,phone,pin)
        create_recover = self.db_instance.create_passphrase(email,recover_phrase)
        if user is False:
            print("Error")
            return 
        if create_recover is False:
            print("Error")
            return 

        login_page_window = tk.Toplevel(self.master)
        login_page = cus_login.LoginPage(login_page_window)
        self.master.withdraw()