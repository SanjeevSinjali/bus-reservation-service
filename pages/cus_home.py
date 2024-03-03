import tkinter as tk
from tkinter import ttk,Radiobutton,filedialog
from tkcalendar import Calendar,DateEntry
from lib import globals,dbfunctions,createticket
from pages import cus_login
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
        self.date = self.date_entry.get_date()
        self.tabledatas = self.db_instance.search_travel_from_to(self.leaving_from_str.get(),self.going_to_str.get(),self.date,self.shift.get())
        if self.tabledatas is False:
            tk.messagebox.showerror(title = "Info",message = "Not Available")
            return

        self.clear_frame(self.content_frame)

        self.searchPage()
        
    def clear_table_from_frame(self, frame):
        for widget in frame.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            print(f"Destroying widget: {widget}")  # Debugging output
            widget.destroy()
        print("Frame cleared") 
        
    def searchPage(self):
        welcome_lbl = ttk.Label(self.content_frame, text=f"Welcome Back! {globals.User['fullname']}")
        welcome_lbl.grid(row=0, column=0, columnspan=5, padx=20, pady=10, sticky="e")

        source_lbl = ttk.Label(self.content_frame, text=f"{self.leaving_from_str.get()}")
        source_lbl.grid(row=1, column=0, columnspan=1, padx=0, pady=0, sticky="e")

        separator_lbl = ttk.Label(self.content_frame, text="to")
        separator_lbl.grid(row=1, column=1, columnspan=1, padx=0, pady=0, sticky="e")

        destination_lbl = ttk.Label(self.content_frame, text=f"{self.going_to_str.get()}")
        destination_lbl.grid(row=1, column=2, columnspan=1, padx=0, pady=0, sticky="e")

        shift_lbl = ttk.Label(self.content_frame, text=f"shift: {self.shift.get()}")
        shift_lbl.grid(row=1, column=3, columnspan=1, padx=0, pady=0, sticky="e")

        date_lbl = ttk.Label(self.content_frame, text=f"{self.date}")
        date_lbl.grid(row=1, column=4, columnspan=1, padx=0, pady=0, sticky="e")

        self.tree = ttk.Treeview(self.content_frame, columns=("Travels", "Bus Type", "Departure/Shift", "Available", "Fare"),height=24)
        self.tree.heading("#0", text="Id", anchor="w")
        self.tree.heading("Travels", text="Travels")
        self.tree.heading("Bus Type", text="Bus Type")
        self.tree.heading("Departure/Shift", text="Departure/Shift")
        self.tree.heading("Available", text="Available")
        self.tree.heading("Fare", text="Fare")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Travels", width=150)  # Adjust the width as needed
        self.tree.column("Bus Type", width=100)  # Adjust the width as needed
        self.tree.column("Departure/Shift", width=100)  # Adjust the width as needed
        self.tree.column("Available", width=75)  # Adjust the width as needed
        self.tree.column("Fare", width=75)  # Adjust the width as needed

        for row_data in self.tabledatas:
            self.tree.insert("", "end", values=row_data)

        self.tree.grid(row=2, column=0, columnspan=5,padx=10, pady=0)
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)


    def on_treeview_select(self, event):
        selected_item = self.tree.selection()
        
        if selected_item:
            # Get the values of the selected row
            values = self.tree.item(selected_item, 'values')
            # Now you have the values, you can use them to navigate to another frame or perform other actions
            print("Selected Row Values:", values)
            bus_id = values[-1]
            # print(values[-1])
            self.clear_table_from_frame(self.content_frame)
        self.book_page(bus_id)

    def book_page(self,bus_id):
        img_label = tk.Label(self.content_frame)
        # img = tk.PhotoImage(file="/Users/sanjeev/Desktop/ticket/data/images/bus seat.png")
        img = tk.PhotoImage(file=globals.dataPath+"/bus seat.png")
        img_label.config(image=img)
        img_label.image = img
        img_label.grid(row=3, column=0, pady=10, sticky="w")

        self.bookdatas = self.db_instance.get_all_bus_seat_from_bus_id(bus_id)
        print(self.bookdatas)

        self.tree = ttk.Treeview(self.content_frame, columns=("Seat Number", "Status","Bus_id","price"),height=24)
        self.tree.heading("#0", text="Id", anchor="w")
        self.tree.heading("Seat Number", text="Seat Number")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Bus_id",text="Bus_id")
        self.tree.heading("price",text="price")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Seat Number", width=150)  # Adjust the width as needed
        self.tree.column("Status", width=100)
        self.tree.column("Bus_id",width=50)  # Adjust the width as needed
        self.tree.column("price",width=50) 

        for row_data in self.bookdatas:
            self.tree.insert("", "end", values=row_data)

        self.tree.grid(row=3, column=1, columnspan=5,padx=10, pady=0)

        book_btn = ttk.Button(self.content_frame, text="Book", command=self.book_selected)
        book_btn.grid(row=4, column=3, padx=10, pady=10, sticky="e")
        
    def book_selected(self):
        selected_items = self.tree.selection()
        self.a = {
            "seats": [],
            "bus_id": "",
        }
        if selected_items:
            for item in selected_items:
                values = self.tree.item(item, 'values')
                if values[1] == "BOOKED":
                    tk.messagebox.showerror(title = "Error",message = f'Seat Number : {values[0]} already booked!!!')
                    self.tree.selection_remove(item)
                    return 
                else:
                    self.a["seats"].append(int(values[0]))
                    self.a["bus_id"] = values[2]
                print("Selected Row Values:", values)
        else:
            print("No rows selected.")
        # self.destroy()
        self.clear_frame(self.content_frame)
        self.final_book_page()
        
    def final_book_page(self):
        self.total = 0

        self.oneprice = self.bookdatas[0][3][0][0]
        for i in self.a["seats"]:
            self.total = self.total + self.oneprice
        
        payment_lbl = ttk.Label(self.content_frame, text=f"Payment")
        payment_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        seats_lbl = ttk.Label(self.content_frame, text=f"Seats: {self.a['seats']}")
        seats_lbl.grid(row=1, column=0, padx=20, pady=10, sticky="e")

        bus_lbl = ttk.Label(self.content_frame, text=f"Bus_id: {self.a['bus_id']}")
        bus_lbl.grid(row=2, column=0, padx=20, pady=10, sticky="e")

        price_lbl = ttk.Label(self.content_frame, text=f"Total Price: {self.total}")
        price_lbl.grid(row=3, column=0, padx=20, pady=10, sticky="e")

        price_lbl = ttk.Label(self.content_frame, text=f"TransactionPin :")
        price_lbl.grid(row=4, column=0, padx=20, pady=10, sticky="e")

        self.transaction_pin = ttk.Entry(self.content_frame)
        self.transaction_pin.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        book_btn = ttk.Button(self.content_frame, text="Book", command=self.final_book_selected)
        book_btn.grid(row=5, column=3, padx=10, pady=10, sticky="e")

    def final_book_selected(self):
        self.date
        pin = self.transaction_pin.get()
        bus_id = self.a["bus_id"]
        user_id = globals.User["id"]
        get_pin_from_user = self.db_instance.cursor.execute('''SELECT pin FROM user where id=?''',(user_id,)).fetchone()
        # print(get_pin_from_user[0])
        if int(pin) != get_pin_from_user[0]:
                tk.messagebox.showerror(title = "Error",message = "Pin Incorrect!!")
                return 
        try:
            for i in self.a["seats"]:
                booking_date = self.date
                bus_seat_ids = self.a["seats"]
                total_amount = self.total
                print(user_id,bus_id,booking_date,total_amount)
                self.db_instance.cursor.execute('INSERT INTO booking(user_id,bus_id,bus_seat_number,booking_date,total_amount) VALUES(?,?,?,?,?)',(user_id,bus_id,i,booking_date,self.oneprice))
                self.db_instance.conn.commit()

            for i in self.a["seats"]:
                self.db_instance.cursor.execute('UPDATE busseat SET isAvailable=? where seatnumber=?',(0,i))
                self.db_instance.conn.commit()


            tk.messagebox.showinfo(title = "Success",message = "Payment Success!!! \n Generating ticket")

            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

            if file_path:
                ticket_pdf = createticket.TicketPDF(seats=self.a["seats"], bus_id=bus_id, total_amount=total_amount,
                                       username=globals.User["fullname"],file_path=file_path)
                ticket_pdf.generate_pdf()

        except Exception as e:
                print(e)
                tk.messagebox.showerror(title = "Error",message = "Couldn't process!!")
                return 
        tk.messagebox.showinfo(title = "Success",message = "Ticket Generated")
        
        self.a = {}
        
    def settingPage(self):
        user = self.db_instance.get_one_user_info(globals.User["id"])
        if user is False:
            return  tk.messagebox.showerror(title = "Error",message = "Error getting data!!!")
        
        self.fullname = tk.StringVar()
        self.email = tk.StringVar()
        self.phonenumber = tk.StringVar()
        self.password = tk.StringVar()
        
        register_lbl = ttk.Label(self.content_frame,text="Register")
        register_lbl.grid(row=0, column=1,padx=0, pady=10, sticky="e")
        
        ttk.Label(self.content_frame, text="Full Name:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_fullname = ttk.Entry(self.content_frame,textvariable=self.fullname)
        self.entry_fullname.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.fullname.set(user[0])

        ttk.Label(self.content_frame, text="Email:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_email = ttk.Entry(self.content_frame,textvariable=self.email)
        self.entry_email.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.email.set(user[1])

        ttk.Label(self.content_frame, text="Phone Number:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.entry_phone = ttk.Entry(self.content_frame,textvariable=self.phonenumber)
        self.entry_phone.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.phonenumber.set(user[2])

        ttk.Label(self.content_frame, text="Password:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.entry_password = ttk.Entry(self.content_frame, show="*",textvariable=self.password)
        self.entry_password.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.password.set(user[3])

        # Buttons
        ttk.Button(self.content_frame, text="Update", command=self.update_user).grid(row=6, column=1, padx=10, pady=10, sticky="e")

    def update_user(self):
        user_id = globals.User["id"]
        fullname = self.fullname.get()
        email = self.email.get()
        phonenumber = self.phonenumber.get()
        password = self.password.get()
        print(fullname,password,email,phonenumber,user_id)
        update_user = self.db_instance.update_user(fullname,password,email,phonenumber,user_id)
        if update_user:
            return tk.messagebox.showerror(title = "Info",message = "Update Success")
        else: 
            return tk.messagebox.showerror(title = "Error",message = "Failed!!!")
        
    def handle_dashboard_click(self, clicked_button):
        if clicked_button == "Home":
            self.clear_frame(self.content_frame)
            self.HPage()
            print("Handling Home button click in HomePage")
        elif clicked_button == "History":
            self.clear_frame(self.content_frame)
            self.HistoryPage()
            print("Handling History button click in HomePage")
        elif clicked_button == "Settings":
            print("Handling Settings button click in HomePage")
            self.clear_frame(self.content_frame)
            self.settingPage()
        elif clicked_button == "Logout":
            print("Handling Logout button click in HomePage")
            globals.User = {}
            login_page_window = tk.Toplevel(self.master)
            login_page = cus_login.LoginPage(login_page_window)
            self.master.withdraw() 
            
    def HistoryPage(self):
        self.tree = ttk.Treeview(self.content_frame, columns=("busseat_number", "booking_date", "total_amount"),show="headings")
        self.tree.heading("busseat_number", text="busseat_number")
        self.tree.heading("booking_date", text="booking_date")
        self.tree.heading("total_amount", text="total_amount")

        self.tree.column("busseat_number", width=100)  # Adjust the width as needed
        self.tree.column("booking_date", width=75)  # Adjust the width as needed
        self.tree.column("total_amount", width=75)  # Adjust the width as needed

        rows_data = self.db_instance.cursor.execute('SELECT bus_seat_number,booking_date,total_amount FROM booking where user_id=?',(globals.User["id"],)).fetchall()

        
        for row_data in rows_data:
            self.tree.insert("", "end", values=row_data)

        self.tree.pack(fill="both",expand=True)

    def get_source_destination_list(self): 
        data_list = self.db_instance.get_all_destination_source()
        source = []
        destination = []
        if list == None:
            print(False)
        else:            
            for i in data_list:
                source.append(i[0])
                destination.append(i[1])
        self.source_list = list(set(source))
        self.destination_list = list(set(destination))