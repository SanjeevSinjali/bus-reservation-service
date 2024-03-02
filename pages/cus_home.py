import tkinter as tk
from tkinter import ttk
from lib import globals
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