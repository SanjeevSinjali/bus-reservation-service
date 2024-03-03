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
    
    #registration function    
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
        

    #Login Page
    def has_user(self, fullname, password,role=None):
        fullname = fullname.strip()
        password = password.strip()
        print(role)
        if role is None:
            print("hello none")
            user = self.cursor.execute(
                'SELECT id,fullname,role FROM user WHERE fullname=? and password=?',
                (fullname, password)).fetchone()
        else: 
            user = self.cursor.execute(
                'SELECT id,fullname,role FROM user WHERE fullname=? and password=? and role=?',
                (fullname, password, role)).fetchone()
        if user is None:
            return None
        else:
            return user    
    
    #admin get all user
    def get_all_user_info(self):
        list = []
        rows = self.cursor.execute("SELECT id, fullname, password , email, role FROM user WHERE role NOT 'ADMIN'")
        for item in rows:
            list.append({
                'id': item[0],
                'fullname': item[1],
                'password': item[2],
                'email': item[3],
                'role': item[4]
            })
        return list
    
    #get single user info
    def get_one_user_info(self,user_id):
        print(user_id)
        print(type(user_id))
        user = self.cursor.execute("SELECT fullname, email , phonenumber , password FROM user WHERE id=?",(user_id,)).fetchone()
        print(user)
        if user is None:
            return False
        else :
            return user

    # create passphrase for a user --> used for recovery 
    def create_passphrase(self,email,passphrase):
        try:
            self.cursor.execute('INSERT INTO recover(email,recover_phrase) VALUES(?,?)',(email,passphrase))
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        
    def forgot_password(self,email,recover_phrase,new_password):
        try:
            phrase = self.cursor.execute('SELECT recover_phrase FROM recover WHERE email=?',(email,)).fetchone()
            if phrase is None:
                return False
            if phrase[0] != recover_phrase:
                return False 
            self.cursor.execute('UPDATE user SET password=? WHERE email=?',(new_password,email))
            self.conn.commit()
            return True

        except Exception as e:
            print(e)
            return False 
        
    #get data from user using their roles
    def get_user_by_role(self, role):
        if role == "STAFF":
            user_data = self.cursor.execute("""
                SELECT u.fullname, u.email, u.phonenumber, u.agency_id, a.name
                FROM user u
                LEFT JOIN agency a ON u.agency_id = a.id
                WHERE u.role=?
            """, (role,)).fetchall()
        else:
            user_data = self.cursor.execute("""
                SELECT fullname, email, phonenumber
                FROM user
                WHERE role=?""", (role,)).fetchall()

        if user_data is None:
            return False
        else:
            print(user_data)
            return user_data
        
    #search function for customer  
    def search_travel_from_to(self, source, destination, date, shift):
        self.cursor.execute('SELECT type, shift, status, seat_price,id, agency_id FROM bus WHERE source=? AND destination=? AND operate_date=? AND shift=?', (source, destination, date, shift))
        travels = self.cursor.fetchall()
        print("Number of results:", len(travels))

        if not travels:
            return False

        for i in range(0, len(travels)):
            agency_id = int(travels[i][5])
            self.cursor.execute('SELECT name FROM agency WHERE id=?',(agency_id,))
            agency_name = self.cursor.fetchone()
            travels[i] = agency_name + travels[i]
        print(travels)
        return travels