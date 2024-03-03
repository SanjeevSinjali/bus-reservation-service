import tkinter as tk
from tkinter import Radiobutton, ttk
from pages import cus_login
from lib import globals
from tkcalendar import Calendar,DateEntry
from lib import dbfunctions
from tkcalendar import Calendar,DateEntry
import datetime


class Dashboard(tk.Frame):
    def __init__(self, master=None, button_callback=None):
        super().__init__(master)
        self.master = master

        self.selected_button = tk.StringVar(value="Home")  # Variable to store the selected button

        img_label = tk.Label(self)
        img_label.pack(side="top", pady=10)
        img = tk.PhotoImage(file=globals.dataPath+"/logo.png")
        img_label.config(image=img)
        img_label.image = img
        self.button_callback = button_callback

        self.btn_home = ttk.Button(self, text="Home", command=lambda: self.button_clicked("Home"))
        self.btn_home.pack(side="top", fill="x", padx=10, pady=5)

        self.btn_history = ttk.Button(self, text="Orders", command=lambda: self.button_clicked("Orders"))
        self.btn_history.pack(side="top", fill="x", padx=10, pady=5)

        self.btn_settings = ttk.Button(self, text="Settings", command=lambda: self.button_clicked("Settings"))
        self.btn_settings.pack(side="top", fill="x", padx=10, pady=5)

        self.btn_Logout = ttk.Button(self, text="Logout", command=lambda: self.button_clicked("Logout"))
        self.btn_Logout.pack(side="top", fill="x", padx=10, pady=5)

    def button_clicked(self, clicked):
            if self.button_callback:
                self.button_callback(clicked)
                
class StaffPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.db_instance = dbfunctions.dbfunctions()
        self.master.title("Staff Page")
        self.master.geometry("1000x700")
        self.master.resizable(False, False)

        self.dashboard = Dashboard(self, button_callback=self.handle_dashboard_click)
        self.dashboard.pack(side="left", fill="y", expand=True)

        self.get_source_destination_list()

        self.staff_content_frame = tk.Frame(self.master)
        self.staff_content_frame.pack(side="right", fill="both", expand=True)

        welcome_lbl = ttk.Label(self.staff_content_frame, text=f"Welcome Back!")
        welcome_lbl.pack(side="top")

        self.SPage()

    def SPage(self):
        user_id = globals.User["id"]
        self.customer_tree = ttk.Treeview(self.staff_content_frame,columns=("Type","Source", "Destination","Numberofseats"), show="headings")
        self.customer_tree.heading("Type", text="Type")
        self.customer_tree.heading("Source", text="Source")
        self.customer_tree.heading("Destination", text="Destination")
        self.customer_tree.heading("Numberofseats", text="Numberofseats")

        bus_data = self.db_instance.get_all_bus_info(user_id) 

        for bus in bus_data:
            self.customer_tree.insert("", "end", values=(bus['type'], bus['source'], bus['destination'], bus['seatsno'],bus['departtime'],bus['operate_date'],bus['status'],bus['shift'],bus['seatprice'],bus['id']))

        self.customer_tree.pack(fill="both",expand=True)
        self.customer_tree.bind("<<TreeviewSelect>>", self.on_treeview_select)


    def on_treeview_select(self, event):
        selected_item = self.customer_tree.selection()
        
        if selected_item:
            # Get the values of the selected row
            values = self.customer_tree.item(selected_item, 'values')
            # Now you have the values, you can use them to navigate to another frame or perform other actions
            print("Selected Row Values:", values)
            self.selected_bus_id = values[-1]
            print("selected_bus : ",self.selected_bus_id)
            self.clear_frame(self.staff_content_frame)
        self.update_bus_details_table(values)

    def clear_table_from_frame(self, frame):
        for widget in frame.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()  

    def update_bus_details_table(self,bus_details):
        print("bus_details : ",bus_details)
        depart_lbl = tk.Label(self.staff_content_frame,text="Depart Time : ")
        depart_lbl.grid(row=1,column=1)

        self.depart_time = tk.StringVar(value=bus_details[4])
        R1 = Radiobutton(self.staff_content_frame, text="4PM", variable=self.depart_time, value="4PM", command=lambda: self.depart_time.set("4PM"))
        R1.grid(row=2,column=2)
        R2 = Radiobutton(self.staff_content_frame, text="6AM", variable=self.depart_time, value="6AM", command=lambda: self.depart_time.set("6AM"))
        R2.grid(row=2,column=3)

        source_lbl = tk.Label(self.staff_content_frame,text="From : ")
        source_lbl.grid(row=3,column=1,pady=20)

        self.leaving_from_str = tk.StringVar(value=bus_details[1]) 
        leaving_from = ttk.Combobox(self.staff_content_frame, width=27, textvariable=self.leaving_from_str) 
        # leaving_from['values'] = ('KATHMANDU', 'SURKHET', 'POKHARA', 'KAKARBHITTA', 'ITAHARI', 'NEPALGUNJ', 'BUTWAL', 'CHITWAN') 
        leaving_from['values'] = self.source_list

        leaving_from.grid(column=3, row=3)

        destination_lbl = tk.Label(self.staff_content_frame,text="To : ")
        destination_lbl.grid(row=4,column=1)

        self.going_to_str = tk.StringVar(value=bus_details[2]) 
        going_to = ttk.Combobox(self.staff_content_frame, width=27, textvariable=self.going_to_str) 
        # going_to['values'] = ('KATHMANDU', 'SURKHET', 'POKHARA', 'KAKARBHITTA', 'ITAHARI', 'NEPALGUNJ', 'BUTWAL', 'CHITWAN') 
        going_to['values'] = self.destination_list

        going_to.grid(column=3, row=4)

        operate_date = tk.Label(self.staff_content_frame,text="Operation date : ")
        operate_date.grid(row=5,column=1)

        # Parse the date string and convert it to the desired format
        date_str = bus_details[5]
        print(date_str)
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        print("date-obj: ",date_obj)
        self.date_entry = DateEntry(self.staff_content_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.set_date(date_obj)
        self.date_entry.grid(row=5, column=3, sticky="w")

        shift_lbl = tk.Label(self.staff_content_frame,text="Shift  : ")
        shift_lbl.grid(row=6,column=1)

        self.shift = tk.StringVar(value=bus_details[7])
        R1 = Radiobutton(self.staff_content_frame, text="Day", variable=self.shift, value="DAY", command=lambda: self.shift.set("DAY"))
        R1.grid(row=7,column=2)
        R2 = Radiobutton(self.staff_content_frame, text="Night", variable=self.shift, value="NIGHT", command=lambda: self.shift.set("NIGHT"))
        R2.grid(row=7,column=3)

        seat_price_lbl = tk.Label(self.staff_content_frame,text="Seat price  : ")
        seat_price_lbl.grid(row=8,column=1)

        self.seat_price_data = ttk.Entry(self.staff_content_frame)
        self.seat_price_data.insert(0,bus_details[8])
        self.seat_price_data.grid(row=8, column=2, sticky="w")
    
        status_lbl = tk.Label(self.staff_content_frame,text="Status  : ")
        status_lbl.grid(row=9,column=1)

        self.status_bus = tk.StringVar(value=bus_details[6])
        R1 = Radiobutton(self.staff_content_frame, text="ACTIVE", variable=self.status_bus, value="ACTIVE", command= lambda: self.status_bus.set("ACTIVE"))
        R1.grid(row=10,column=2)
        R2 = Radiobutton(self.staff_content_frame, text="INACTIVE", variable=self.status_bus, value="INACTIVE", command=lambda: self.status_bus.set("INACTIVE"))
        R2.grid(row=10,column=3)

        self.update_btn = ttk.Button(self.staff_content_frame,text="Update", command=self.update_bus)
        self.update_btn.grid(row=11,column=3)

    def update_bus(self):
        print("updated!!")
        updated_depart_time = self.depart_time.get()
        updated_source = self.leaving_from_str.get()
        updated_destination = self.going_to_str.get()
        updated_date = self.date_entry.get()
        date_obj = datetime.datetime.strptime(updated_date, "%m/%d/%y")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        updated_shift = self.shift.get()
        updated_seat_price = self.seat_price_data.get()
        updated_status_bus = self.status_bus.get()
        bus_id = self.selected_bus_id
        try: 
            self.db_instance.cursor.execute('''UPDATE bus SET departtime=?,source=?,
                                            destination=?,operate_date=?,shift=?,
                                            seat_price=?,status=? WHERE 
                                            id=?''',(updated_depart_time,
                                                    updated_source,
                                                    updated_destination,
                                                    formatted_date,
                                                    updated_shift,
                                                    updated_seat_price,
                                                    updated_status_bus,bus_id))
            self.db_instance.conn.commit()
            tk.messagebox.showinfo(title = "Success",message = "Update Successfully!!!")

        except Exception as e:
                tk.messagebox.showerror(title = "Error",message = "Update Failed!!!")
                return

    def handle_dashboard_click(self, clicked_button):
        if clicked_button == "Home":
            self.clear_frame(self.staff_content_frame)
            self.SPage()
            print("Handling Home button click in HomePage")
        elif clicked_button == "Orders":
            self.clear_frame(self.staff_content_frame)
            self.orderPage()
            print("Handling History button click in HomePage")
        elif clicked_button == "Settings":
            print("Handling Settings button click in HomePage")
            self.clear_frame(self.staff_content_frame)
            self.settingPage()
        elif clicked_button == "Logout":
            print("Handling Logout button click in HomePage")
            globals.User = {}
            login_page_window = tk.Toplevel(self.master)
            login_page = cus_login.LoginPage(login_page_window)
            self.master.withdraw() 
            
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            print(f"Destroying widget: {widget}")  # Debugging output
            widget.destroy()
        print("Frame cleared")  
    
    def orderPage(self):
        user_id = int(globals.User["id"])
        self.tree = ttk.Treeview(self.staff_content_frame, columns=("busseat_number", "booking_date", "total_amount"),show="headings")
        self.tree.heading("busseat_number", text="busseat_number")
        self.tree.heading("booking_date", text="booking_date")
        self.tree.heading("total_amount", text="total_amount")

        self.tree.column("busseat_number", width=100) 
        self.tree.column("booking_date", width=75)  
        self.tree.column("total_amount", width=75)  


        rows_data = self.db_instance.cursor.execute('''SELECT booking.bus_seat_number, booking.booking_date, booking.total_amount
                                                        FROM booking
                                                        JOIN bus ON booking.bus_id = bus.id
                                                        JOIN agency ON bus.agency_id = agency.id
                                                        WHERE agency.id = (SELECT agency_id FROM user WHERE id = ?);''',(user_id,)).fetchall()
        print(rows_data)
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