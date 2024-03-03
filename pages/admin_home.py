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