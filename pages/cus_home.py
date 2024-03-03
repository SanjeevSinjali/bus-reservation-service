import tkinter as tk
from tkinter import ttk,Radiobutton
from tkcalendar import Calendar,DateEntry
from lib import globals,dbfunctions
class Dashboard(tk.Frame):
    def __init__(self, master=None, button_callback=None):
            super().__init__(master)
            self.master = master

            self.selected_button = tk.StringVar(value="Home")
            # Image at the top
            img_label = tk.Label(self)
            img_label.pack(side="top", pady=10)
            # img = tk.PhotoImage(file="/Users/sanjeev/Desktop/ticket/data/images/logo.png")
            img = tk.PhotoImage(file= globals.dataPath+"/logo.png")
            img_label.config(image=img)
            img_label.image = img
            self.button_callback = button_callback

            self.btn_home = ttk.Button(self, text="Home", command=lambda: self.button_clicked("Home"))
            self.btn_home.pack(side="top", fill="x", padx=10, pady=5)

            self.btn_history = ttk.Button(self, text="History", command=lambda: self.button_clicked("History"))
            self.btn_history.pack(side="top", fill="x", padx=10, pady=5)

            self.btn_settings = ttk.Button(self, text="Settings", command=lambda: self.button_clicked("Settings"))
            self.btn_settings.pack(side="top", fill="x", padx=10, pady=5)

            self.btn_settings = ttk.Button(self, text="Logout", command=lambda: self.button_clicked("Logout"))
            self.btn_settings.pack(side="top", fill="x", padx=10, pady=5)

    def button_clicked(self, clicked):
            if self.button_callback:
                self.button_callback(clicked)
                
class HomePage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.db_instance = dbfunctions.dbfunctions()

        self.master.title("Customer Page")
        self.master.geometry("800x700")
        self.master.resizable(False, False)

        self.get_source_destination_list()

        self.dashboard = Dashboard(self, button_callback=self.handle_dashboard_click)
        self.dashboard.pack(side="left", fill="y", expand=True)

        self.content_frame = tk.Frame(self.master)
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.HPage()

    def HPage(self):

        # Content section
        welcome_lbl = ttk.Label(self.content_frame, text=f"Welcome Back! {globals.User['fullname']}")
        welcome_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        # self.content_frame.place(relx=0.5, rely=0.4, relwidth=0.5, relheight=0.4)

        lbl_leaving_from = ttk.Label(self.content_frame, text="Leaving From:")
        lbl_leaving_from.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        # Combobox for Leaving From
        self.leaving_from_str = tk.StringVar() 
        leaving_from = ttk.Combobox(self.content_frame, width=27, textvariable=self.leaving_from_str) 
        # leaving_from['values'] = ('KATHMANDU', 'SURKHET', 'POKHARA', 'KAKARBHITTA', 'ITAHARI', 'NEPALGUNJ', 'BUTWAL', 'CHITWAN') 
        leaving_from['values'] = self.source_list

        leaving_from.grid(column=3, row=1)
        # leaving_from.current(1)

        lbl_going_to = ttk.Label(self.content_frame, text="Going To:")
        lbl_going_to.grid(row=2, column=2, padx=10, pady=10, sticky="e")

        # Combobox for Going To
        self.going_to_str = tk.StringVar() 
        going_to = ttk.Combobox(self.content_frame, width=27, textvariable=self.going_to_str) 
        # going_to['values'] = ('KATHMANDU', 'SURKHET', 'POKHARA', 'KAKARBHITTA', 'ITAHARI', 'NEPALGUNJ', 'BUTWAL', 'CHITWAN') 
        going_to['values'] = self.destination_list
        going_to.grid(column=3, row=2)
        # going_to.current(0)

        travel_date = ttk.Label(self.content_frame,text="Travel Date")
        travel_date.grid(row=3,column=2, padx=10, pady=10, sticky="e")

        # self.date = tk.StringVar()
        self.date_entry = DateEntry(self.content_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=3, column=3, padx=10, pady=10, sticky="w")
        
        shift_selection = ttk.Label(self.content_frame,text="Select Shifts")
        shift_selection.grid(row=4,column=2, padx=10, pady=10, sticky="e")

        self.shift = tk.StringVar()
        R1 = Radiobutton(self.content_frame, text="Day", variable=self.shift, value="DAY", command=self.shift.set("DAY"))
        R1.grid(row=5,column=2)
        R2 = Radiobutton(self.content_frame, text="Night", variable=self.shift, value="NIGHT", command=self.shift.set("NIGHT"))
        R2.grid(row=5,column=3)

        btn_search_acc = ttk.Button(self.content_frame, text="Search", command=self.search)
        btn_search_acc.grid(row=6, column=3, padx=10, pady=10, sticky="e")
        
def search(self):
        print("Search Container")