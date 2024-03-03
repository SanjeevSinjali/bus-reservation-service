# here every functions relating to database is created
import os
import sqlite3
# from globals import User
class dbfunctions(object):
    def __init__(self, db_path=None):
        if db_path is None:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(current_directory, 'database.db')
        else:
            self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()


    def create_database(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS agency (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                status TEXT CHECK(status IN ('ACTIVE', 'INACTIVE')) NOT NULL
                                )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                                id INTEGER PRIMARY KEY,
                                email TEXT UNIQUE NOT NULL,
                                fullname TEXT NOT NULL,
                                password TEXT NOT NULL,
                                pin INTEGER,
                                agency_id INTEGER,
                                phonenumber INTEGER NOT NULL,
                                role TEXT CHECK(role IN ('ADMIN', 'STAFF', 'CUSTOMER')) NOT NULL,
                                FOREIGN KEY (agency_id) REFERENCES agency(id))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS recover (
                                id INTEGER PRIMARY KEY,
                                email TEXT UNIQUE NOT NULL,
                                recover_phrase TEXT NOT NULL,
                                FOREIGN KEY (email) REFERENCES user(email)
                                )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bus(
                                id INTEGER PRIMARY KEY,
                                type TEXT NOT NULL,
                                seatsno INTEGER NOT NULL,
                                departtime TEXT NOT NULL,
                                destination TEXT NOT NULL,
                                source TEXT NOT NULL,
                                operate_date DATE NOT NULL,
                                shift TEXT NOT NULL,
                                seat_price INTEGER NOT NULL,
                                status TEXT CHECK(status IN ('ACTIVE', 'INACTIVE')) NOT NULL,
                                agency_id INTEGER,
                                FOREIGN KEY (agency_id) REFERENCES agency(id)
                                )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS busseat(
                                id INTEGER PRIMARY KEY,
                                bus_id INTEGER,
                                isAvailable INTEGER NOT NULL CHECK(isAvailable IN (0, 1)),
                                seatnumber INTEGER NOT NULL,
                                FOREIGN KEY (bus_id) REFERENCES bus(id)
                                )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS booking (
                                id INTEGER PRIMARY KEY,
                                user_id INTEGER,
                                bus_seat_number INTEGER NOT NULL,
                                bus_id INTEGER NOT NULL,
                                booking_date TEXT NOT NULL,
                                total_amount INTEGER NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES user(id),
                                FOREIGN KEY (bus_id) REFERENCES bus(id)
                                )''')
        self.conn.commit()
        # self.conn.close()
        
    def create_user(self, fullname, password,email,phonenumber,pin,agency_name=None,role="CUSTOMER",):
        print(agency_name)
        print(role)
        fullname = fullname.strip()
        password = password.strip()
        email = email.strip()
        phonenumber = int(phonenumber)
        if pin is not None:
            pin = int(pin)
        if agency_name is not None:
            agency_name = agency_name.strip()     
        role = role.strip()
        try:
            if agency_name is not None:
                agency_id = self.cursor.execute('SELECT id FROM agency where name=?',(agency_name,)).fetchone()
                self.cursor.execute('INSERT INTO user(email, fullname, password,phonenumber,role,agency_id) VALUES(?,?,?,?,?,?)', (email ,fullname, password , phonenumber,role,agency_id[0]))
            else:
                self.cursor.execute('INSERT INTO user(email, fullname, password,phonenumber,role,pin) VALUES(?,?,?,?,?,?)', (email ,fullname, password , phonenumber, role,pin))
            self.conn.commit()
            return True
        except Exception as e :
            print(f"Error during insertion: {e}")
            return False
        