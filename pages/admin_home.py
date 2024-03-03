import tkinter as tk
from tkinter import Radiobutton, ttk
from pages import login
from lib import globals
from tkcalendar import Calendar,DateEntry
from lib import dbfunctions

class Dashboard(tk.Frame):
    def __init__(self, master=None, button_callback=None):
        super().__init__(master)
        self.master = master

        self.selected_button = tk.StringVar(value="Home")  # Variable to store the selected button

        # Image at the top
        img_label = tk.Label(self)
        img_label.pack(side="top", pady=10)
        img = tk.PhotoImage(file=globals.dataPath+"/logo.png")
        img_label.config(image=img)
        img_label.image = img
        self.button_callback = button_callback

        # Buttons in a column
        self.btn_home = ttk.Button(self, text="Home", command=lambda: self.button_clicked("Home"))
        self.btn_home.pack(side="top", fill="x", padx=10, pady=5)

        self.btn_create_agency = ttk.Button(self, text="Create Agency", command=lambda: self.button_clicked("createAgency"))
        self.btn_create_agency.pack(side="top", fill="x", padx=10, pady=5)

        self.btn_Logout = ttk.Button(self, text="Logout", command=lambda: self.button_clicked("Logout"))
        self.btn_Logout.pack(side="top", fill="x", padx=10, pady=5)

    def button_clicked(self, clicked):
            if self.button_callback:
                self.button_callback(clicked)

class AdminPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.db_instance = dbfunctions.dbfunctions()
        self.master.title("Admin Page")
        self.master.geometry("1000x700")
        self.master.resizable(False, False)

        self.dashboard = Dashboard(self, button_callback=self.handle_dashboard_click)
        self.dashboard.pack(side="left", fill="y", expand=True)

        self.admin_content_frame = tk.Frame(self.master)
        self.admin_content_frame.pack(side="right", fill="both", expand=True)

        self.APage()

    def APage(self):

        # Content section
        welcome_lbl = ttk.Label(self.admin_content_frame, text=f"Welcome Back!")
        welcome_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        Customers_lbl = ttk.Label(self.admin_content_frame, text=f"Customers")
        Customers_lbl.grid(row=1, column=0, padx=0, pady=10, sticky="e")
        # Customer Table
        customer_frame = tk.Frame(self.admin_content_frame)
        customer_frame.grid(row=2, column=0, columnspan=3,padx=10, pady=10, sticky="nsew")

        customer_tree = ttk.Treeview(customer_frame, columns=("Full Name", "Email", "Phone Number"), show="headings")
        customer_tree.heading("Full Name", text="Full Name")
        customer_tree.heading("Email", text="Email")
        customer_tree.heading("Phone Number", text="Phone Number")

        #Fetch customer data from the database and populate the table
        customers = self.db_instance.get_user_by_role("CUSTOMER")
        for customer in customers:
            customer_tree.insert("", "end", values=(customer[0], customer[1], customer[2]))

        customer_tree.pack(fill="both", expand=True)

        Staff_lbl = ttk.Label(self.admin_content_frame, text=f"Staff")
        Staff_lbl.grid(row=3, column=0, padx=0, pady=10, sticky="e")

        # Staff Table
        staff_frame = tk.Frame(self.admin_content_frame)
        staff_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        staff_tree = ttk.Treeview(staff_frame, columns=("Full Name", "Email", "Phone Number", "Agency"), show="headings")
        staff_tree.heading("Full Name", text="Full Name")
        staff_tree.heading("Email", text="Email")
        staff_tree.heading("Phone Number", text="Phone Number")
        staff_tree.heading("Agency", text="Agency")

        # self.db_instance.get_user_by_role("STAFF")
        # self.db_instance.get_user_by_role("CUSTOMER")
        # Fetch staff data from the database and populate the table
        staff_members = self.db_instance.get_user_by_role("STAFF")  # Assuming you have a method to fetch staff
        for staff_member in staff_members:
            staff_tree.insert("", "end", values=(staff_member[0], staff_member[1], staff_member[2],staff_member[4]))

        staff_tree.pack(fill="both", expand=True)
        
    def handle_dashboard_click(self, clicked_button):
        if clicked_button == "Home":
            self.clear_frame(self.admin_content_frame)
            self.APage()
            print("Handling Home button click in HomePage")
        elif clicked_button == "Logout":
            print("Handling Logout button click in HomePage")
            globals.User = {}
            login_page_window = tk.Toplevel(self.master)
            login_page = login.LoginPage(login_page_window)
            self.master.withdraw()
        elif clicked_button == "createAgency":
            self.clear_frame(self.admin_content_frame)
            self.create_agency()