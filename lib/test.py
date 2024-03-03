import sys
from globals import User
sys.path.append('/Users/sanjeev/Desktop/ticket/lib/dbfunctions')
from dbfunctions import dbfunctions

# Create an instance of dbfunctions
db_instance = dbfunctions()

# # Create the initial database structure
db_instance.create_database()

db_instance.create_agency("Kakrebihar yatayat","ACTIVE")
db_instance.create_agency("Maddhe pashcim yatayat","ACTIVE")
db_instance.create_agency("Purano bato yatayat","ACTIVE")
db_instance.create_agency("Pokhara yatayat","INACTIVE")

# # Insert a user
db_instance.create_user("admin", "111", "admin@admin.com", 1234567890,None,None ,"ADMIN")
db_instance.create_user("staff", "111", "staff@staff.com", 1234567890,None, "Kakrebihar yatayat" ,"STAFF")
db_instance.create_user("customer", "111", "customer@customer.com", 1234567890, 123)

db_instance.create_passphrase('staff@staff.com','iamstaff')
db_instance.create_passphrase('customer@customer.com','customer')

db_instance.create_bus("DELUXE",19,"4PM","KATHMANDU","SURKHET","2024-03-05","DAY",2000,"ACTIVE",1)
db_instance.create_bus("AC",19,"4PM","SURKHET","KATHMANDU","2024-03-06","NIGHT",2500,"ACTIVE",1)
db_instance.create_bus("DELUXE",19,"6AM","KATHMANDU","SURKHET","2024-03-04","NIGHT",2500,"ACTIVE",2)
db_instance.create_bus("AC",19,"6AM","POKHARA","KATHMANDU","2024-03-08","DAY",2000,"ACTIVE",3)
db_instance.create_bus("DELUXE",19,"4PM","KATHMANDU","POKHARA","2024-03-10","NIGHT",2500,"ACTIVE",1)
db_instance.create_bus("DELUXE",19,"6AM","ITAHARI","KATHMANDU","2024-03-06","DAY",2500,"ACTIVE",3)
db_instance.create_bus("AC",19,"4PM","KATHMANDU","ITAHARI","2024-03-08","NIGHT",2500,"ACTIVE",4)
db_instance.create_bus("DELUXE",19,"4PM","KAKARBHITTA","KATHMANDU","2024-03-06","DAY",3000,"ACTIVE",3)
db_instance.create_bus("AC",19,"6AM","KATHMANDU","KAKARBHITTA","2024-03-09","NIGHT",3000,"ACTIVE",2)