import tkinter as tk
from tkinter import ttk,messagebox
from pages import admin_login,staff_login,cus_home,cus_register
from lib import globals,dbfunctions
class LoginPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.db_instance = dbfunctions.dbfunctions()
        self.master.title("Login Page")
        self.master.geometry("750x700")
        self.master.resizable(False, False)

        img_label = tk.Label(self.master)
        img_label.place(relx=0, rely=0, relwidth=0.5, relheight=1)
        img = tk.PhotoImage(file=globals.dataPath+"/bus.png")
        img_label.config(image=img)
        img_label.image = img

        self.login_frame = tk.Frame(self.master)
        self.login_frame.place(relx=0.5, rely=0.4, relwidth=0.5, relheight=0.4)

        self.init_page()

    def customerPage(self):

        welcome_lbl = ttk.Label(self.login_frame,text="Welcome Back!")
        welcome_lbl.grid(row=0, column=0,padx=0, pady=10, sticky="e")

        btn_create_acc = ttk.Button(self.login_frame, text="Create Account", command=self.createAccount)
        btn_create_acc.grid(row=0, column=1, padx=10, pady=10, sticky="e")

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

        btn_forgot = ttk.Button(self.login_frame, text="Forgot Password", command=self.forgotPassword)
        btn_forgot.grid(row=3, column=0, padx=10, pady=0, sticky="e")
        
        btn_login = ttk.Button(self.login_frame, text="Login", command=self.login)
        btn_login.grid(row=3, column=1, padx=10, pady=0, sticky="e")

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        print("Username:", username)
        print("Password:", password)

        user = self.db_instance.has_user(username, password)
        if user is None:
            tk.messagebox.showerror(title = "Error",message = "User not Found!!!")
            return 

        globals.User["id"] = user[0]
        globals.User["fullname"] = user[1]
        globals.User["role"] = user[2]

        home_page = cus_home.HomePage(self.master)
        home_page.pack(fill="both", expand=True)

        self.destroy()
    
    def init_page(self):

        btn_admin = ttk.Button(self.login_frame, text="ADMIN", command=self.admin)
        btn_admin.grid(row=3, column=0, padx=10, pady=0, sticky="e")
        
        btn_staff = ttk.Button(self.login_frame, text="STAFF", command=self.staff)
        btn_staff.grid(row=3, column=1, padx=10, pady=0, sticky="e")

        btn_staff = ttk.Button(self.login_frame, text="CUSTOMER", command=self.customer)
        btn_staff.grid(row=3, column=2, padx=10, pady=0, sticky="e")


    def admin(self):
        admin_page = admin_login.LoginPage(self.master)
        admin_page.pack(fill="both", expand=True)
        self.destroy()        

    def staff(self):
        staff_page = staff_login.LoginPage(self.master)
        staff_page.pack(fill="both", expand=True)
        self.destroy()
            
    def customer(self):
        self.clear_frame(self)
        self.customerPage()

    def createAccount(self):
        self.destroy()
        signup_page = cus_register.RegisterPage(self.master)
        
    def forgotPassword(self):
        print("You forgot your password!!!!!")

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            print(f"Destroying widget: {widget}")
            widget.destroy()

    def forgotPassword(self):
        self.clear_frame(self.login_frame)
        self.forgotPage()
        print("You forgot your password!!!!!")

    def forgotPage(self):
        email_lbl = ttk.Label(self.login_frame, text="Email")
        email_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.entry_email = ttk.Entry(self.login_frame)
        self.entry_email.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        recover_lbl = ttk.Label(self.login_frame, text="Recover Phrase")
        recover_lbl.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.recover_key = ttk.Entry(self.login_frame)
        self.recover_key.grid(row=2, column=1, padx=10, pady=10, sticky="w")       

        lbl_password = ttk.Label(self.login_frame, text="New Password:")
        lbl_password.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.new_password = ttk.Entry(self.login_frame)
        self.new_password.grid(row=3, column=1, padx=10, pady=10, sticky="w")   

        lbl_reenter_password = ttk.Label(self.login_frame, text="Re-enter Password:")
        lbl_reenter_password.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.re_password = ttk.Entry(self.login_frame)
        self.re_password.grid(row=4, column=1, padx=10, pady=10, sticky="w")    

        btn_forgot = ttk.Button(self.login_frame, text="Recover", command=self.recover)
        btn_forgot.grid(row=5, column=1, padx=10, pady=0, sticky="e")

    def recover(self):
        email = self.entry_email.get().strip()
        phrase = self.recover_key.get().strip()
        password = self.new_password.get().strip()
        re_password = self.re_password.get().strip()
        if password != re_password:
            tk.messagebox.showerror(title = "Error",message = "Password didn't match with each other!!!")
            return
        try:
            recover_password = self.db_instance.forgot_password(email,phrase,password)
            if recover_password:
                tk.messagebox.showinfo(title = "Success",message = "Password Successfully reset")
            else:
                tk.messagebox.showerror(title = "Error",message = "Failed to recover password!!!")

        except Exception as e:
            tk.messagebox.showerror(title = "Error",message = "Failed to recover password!!!")
            return
        self.clear_frame(self.login_frame)
        self.customerPage()