# Libraries
#    tkinter:   Pip install tkinter
#    regex:     Standard
#    sqlite3:   Standard


from tkinter import *
import re
import sqlite3

# regex definitions
date_re = "(?<!.)(\d{4}-\d{2}-\d{2})(?!.)"
phone_re = "(?<!.)(\(\d{3}\) \d{3}-\d{4})(?!.)"
VIN_re = "(?<!.)(([A-Z]|\d){17})(?!.)"
name_re = "(.)+"
desc_re = "(.)+"
custID_re = "(?<!.)(\d{3})(?!.)"


# create tkinter windows
root_window = Tk()
root_window.title("A&P Car Rental Service")
root_window.geometry("1500x950")
root_window.rowconfigure(0,weight=1)
root_window.columnconfigure(0,weight=1)

# connect to the db and create a table
conn = sqlite3.connect("CarRental.db")
print("connected to DB successfully")

# create a cursor
car_rental_c = conn.cursor()


# ====================================================BELOW ARE ALL FUNCTIONS====================================================


def printToConsole(records, columns):
    console.delete(0,console.size())
    numColumns = len(columns)
    numRecords = len(records)
    maxLength = [0]*numColumns
    longest = 0
    temp = ""

    for i in range(numColumns):
        longest = 0
        for j in range (numRecords):
            if(len(str(records[j][i])) > longest): longest = len(str(records[j][i]))
        maxLength[i] = longest

    for i in range(numColumns):
        if(len(columns[i][0]) > maxLength[i]): maxLength[i] = len(columns[i][0]) + 1
        else: maxLength[i] += 1

    for i in range(numColumns):
        temp += columns[i][0]
        if(len(columns[i][0]) < maxLength[i] + 1):
            for j in range (maxLength[i] - len(columns[i][0])):
                temp += " "
    console.insert(0, temp)

    for i in range(numRecords):
        temp = ""
        for r in range(numColumns):
            temp += str(records[i][r])
            if(len(str(records[i][r])) < maxLength[r]):
                for j in range (maxLength[r] - len(str(records[i][r]))):
                    temp += " "
        console.insert(i+1,temp)

    console.insert(console.size(),"Rows returned: " + str(numRecords))

def printToConsoleWithMoney(records, columns):
    console.delete(0,console.size())
    numColumns = len(columns)
    numRecords = len(records)
    maxLength = [0]*numColumns
    longest = 0
    temp = ""

    for i in range(numColumns):
        longest = 0
        for j in range (numRecords):
            if(len(str(records[j][i])) > longest): longest = len(str(records[j][i]))
        maxLength[i] = longest

    for i in range(numColumns):
        if(len(columns[i][0]) > maxLength[i]): maxLength[i] = len(columns[i][0]) + 1
        else: maxLength[i] += 1

    for i in range(numColumns):
        temp += columns[i][0]
        if(len(columns[i][0]) < maxLength[i] + 1):
            for j in range (maxLength[i] - len(columns[i][0])):
                temp += " "
    console.insert(0, temp)

    for i in range(numRecords):
        temp = ""
        for r in range(numColumns):
            if(r == numColumns-1): temp += '$'
            temp += str(records[i][r])
            if(".0" in str(records[i][r])): temp += '0'
            if(len(str(records[i][r])) < maxLength[r]):
                for j in range (maxLength[r] - len(str(records[i][r]))):
                    temp += " "           
        console.insert(i+1,temp)

    console.insert(console.size(),"Rows returned: " + str(numRecords))

# Funcion for creating a Customer
def submitCusty(name, phone):
    insertconn = sqlite3.connect("CarRental.db")
    insert_cur = insertconn.cursor()

    if bool(re.match(phone_re, phone)) and bool(re.match(name_re, name)):
        insert_cur.execute(f"INSERT INTO CUSTOMER(Name, Phone) VALUES('{name}', '{phone}')")
    # commits any changes to the db if any other connections are open
    insertconn.commit()
    insertconn.close()
    
# Function to retreive Customers
def custy_query():
    custy_conn = sqlite3.connect("CarRental.db")
    custy_cur = custy_conn.cursor()
    
    custy_cur.execute("SELECT * FROM Customer")
    
    records = custy_cur.fetchall()
    columns = custy_cur.description

    

    printToConsole(records, columns)

# Function for creating a new pop up window relating to customers
def custyWindow():
    customer_window = Toplevel(root_window)
    customer_window.title("Add Customer")
    customer_window.geometry("500x200")
    customer_window.rowconfigure(0,weight=1)
    customer_window.columnconfigure(0,weight=1)

    customer_label = Label(customer_window, text = "Customer Screen", font = ("ariel", 15))
    customer_label.grid(row = 0, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)
    
    # define labels
    name_label = Label(customer_window, text = "name")
    name_label.grid(row = 1, column = 0, sticky=N+S+E+W)

    phone_label = Label(customer_window, text = "phone")
    phone_label.grid(row = 2, column = 0, sticky=N+S+E+W)

    # define text boxes
    name = Entry(customer_window, width = 30)
    name.grid(row = 1, column = 1, padx = 20)

    phone = Entry(customer_window, width = 30)
    phone.grid(row = 2, column = 1, padx = 20)

    # submit button
    submit_button = Button(customer_window, text = "add customer into the db", command = lambda: submitCusty(name.get(), phone.get()))
    submit_button.grid(row = 3, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

    info_label = Label(customer_window, text = "Add customer into database by inputing name as 'F. Lname', and phone number as "
                                            "'(XXX) XXX-XXXX'. Customer id will be auto generated", font = ("ariel", 8))
    info_label.grid(row = 4, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)



# Function to submit a new vehicle to the DB
def submitVehicle(vehicleID, description, year, vtype, category):
    vehicle_conn = sqlite3.connect("CarRental.db")
    vehicle_cur = vehicle_conn.cursor()

    if (bool(re.match(VIN_re, vehicleID)) and bool(re.match(desc_re, description)) and
        bool(re.match("(\d{4})", year)) and bool(re.match("([1-6]+)", vtype)) and
        bool(re.match("(0|1)", category))):
        vehicle_cur.execute(f"INSERT INTO VEHICLE VALUES('{vehicleID}', '{description}', {year}, {vtype}, {category})")
    # commits any changes to the db if any other connections are open
    vehicle_conn.commit()
    vehicle_conn.close()

# Function to query DB and print vehicles to console
def vehicle_query():
    vehicle_conn = sqlite3.connect("CarRental.db")
    vehicle_cur = vehicle_conn.cursor()
    
    vehicle_cur.execute("SELECT * FROM Vehicle")
    
    records = vehicle_cur.fetchall()
    columns = vehicle_cur.description

    
    
    printToConsole(records, columns)

# Function to create the window to add a new vehicle
def vehicleWindow():
    vehicle_window = Toplevel(root_window)
    vehicle_window.title("Add Vehicle")
    vehicle_window.geometry("600x250")
    vehicle_window.rowconfigure(0,weight=1)
    vehicle_window.columnconfigure(0,weight=1)

    vehicle_label = Label(vehicle_window, text = "Vehicle Screen", font = ("ariel", 15))
    vehicle_label.grid(row = 0, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)
    
    # define labels
    vehicleID_label = Label(vehicle_window, text = "vehicleID")
    vehicleID_label.grid(row = 1, column = 0, sticky=N+S+E+W)

    description_label = Label(vehicle_window, text = "description")
    description_label.grid(row = 2, column = 0, sticky=N+S+E+W)

    year_label = Label(vehicle_window, text = "year")
    year_label.grid(row = 3, column = 0, sticky=N+S+E+W)

    vtype_label = Label(vehicle_window, text = "type")
    vtype_label.grid(row = 4, column = 0, sticky=N+S+E+W)

    category_label = Label(vehicle_window, text = "category")
    category_label.grid(row = 5, column = 0, sticky=N+S+E+W)

    # define text boxes
    vehicleID = Entry(vehicle_window, width = 30)
    vehicleID.grid(row = 1, column = 1, padx = 20) 
    
    description = Entry(vehicle_window, width = 30)
    description.grid(row = 2, column = 1, padx = 20) 
    
    year = Entry(vehicle_window, width = 30)
    year.grid(row = 3, column = 1, padx = 20) 
    
    vtype = Entry(vehicle_window, width = 30)
    vtype.grid(row = 4, column = 1, padx = 20) 
    
    category = Entry(vehicle_window, width = 30)
    category.grid(row = 5, column = 1, padx = 20) 
    
    # Vehicle submit button
    submit_button = Button(vehicle_window, text = "add vehicle into the db", command = lambda: submitVehicle(
                                vehicleID.get(), description.get(), year.get(), vtype.get(), category.get()))
    submit_button.grid(row = 6, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

    info_label = Label(customer_window, text = "Add vehicle into database by inputing VehcicleID as 'XXXXXXXXXXXXXXXXX', "
                                                "description, year as 'YYYY', vechicle type as 'X' (1-6), and category as 'X' (1 or 0)."
                                            , font = ("ariel", 8))
    info_label.grid(row = 7, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)



# Function to submit a new rental
def submitRental(custID, vehicleID, startDate, orderDate, rentalType, 
                    qty, returnDate, paymentDate):
    rental_conn = sqlite3.connect("CarRental.db")
    rental_cur = rental_conn.cursor()

    rental_cur.execute(f"SELECT Weekly, Daily FROM VEHICLE NATURAL JOIN RATE WHERE vehicleID = '{vehicleID}'")
    costs = rental_cur.fetchall()

    if (bool(re.match(custID_re, custID)) and bool(re.match(VIN_re, vehicleID)) and
        bool(re.match(date_re, startDate)) and bool(re.match(date_re, orderDate)) and
        bool(re.match("(1|7)", rentalType)) and bool(re.match("(\d+)", qty)) and
        bool(re.match(date_re, returnDate)) and bool(re.match((date_re +"|NULL"), paymentDate))):

        totalAmount = 0
        
        if(rentalType == '7'): totalAmount = int(qty) * costs[0][0]
        else: totalAmount = int(qty) * costs[0][1]

        returned = 0
        if paymentDate != 'NULL': returned = 1
        rental_cur.execute(f"INSERT INTO RENTAL VALUES('{custID}', '{vehicleID}', '{startDate}', "
                            f"'{orderDate}', '{rentalType}', {qty}, '{returnDate}', {totalAmount}, '{paymentDate}', '{returned}')")
                            
    # commits any changes to the db if any other connections are open
    rental_conn.commit()
    rental_conn.close()

# Function to query and display results of rentals
def rental_query():
    rental_conn = sqlite3.connect("CarRental.db")
    rental_cur = rental_conn.cursor()
    
    rental_cur.execute("SELECT CustID, VehicleID, StartDate, OrderDate, RentalType, "
                       "Qty, ReturnDate, TotalAmount, "
                       "CASE PaymentDate WHEN 'NULL' THEN 'Not-Applicable' ELSE PaymentDate END PaymentDate, "
                       "Returned FROM RENTAL")
    
    records = rental_cur.fetchall()
    columns = rental_cur.description

    printToConsole(records, columns)

def findAvailable(startDate, endDate):
    rental_conn = sqlite3.connect("CarRental.db")
    rental_cur = rental_conn.cursor()

    rental_cur.execute(f"""SELECT R.VEHICLEID AS VIN, V.DESCRIPTION
                        FROM VEHICLE V JOIN RENTAL R ON V.VEHICLEID = R.VEHICLEID
                        WHERE V.VEHICLEID NOT IN (SELECT V.VEHICLEID
                        FROM VEHICLE V JOIN RENTAL R ON V.VEHICLEID = R.VEHICLEID
                        WHERE (STARTDATE BETWEEN "{startDate}" AND "{endDate}") OR 
                        (RETURNDATE BETWEEN "{startDate}" AND "{endDate}") OR 
                        (STARTDATE < "{startDate}" AND RETURNDATE > "{endDate}"))
                        GROUP BY V.VEHICLEID""")
    
    records = rental_cur.fetchall()
    columns = rental_cur.description
    printToConsole(records, columns)

# Window with everything required to make a new rental
def rentalWindow():
    rental_window = Toplevel(root_window)
    rental_window.title("Add Rental")
    rental_window.geometry("500x350")
    rental_window.rowconfigure(0,weight=1)
    rental_window.columnconfigure(0,weight=1)
    
    rental_label = Label(rental_window, text = "Rental Screen", font = ("ariel", 15))
    rental_label.grid(row = 0, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

    # define labels
    startDate_label = Label(rental_window, text = "start date")
    startDate_label.grid(row = 1, column = 0, sticky=N+S+E+W)

    returnDate_label = Label(rental_window, text = "return date")
    returnDate_label.grid(row = 2, column = 0, sticky=N+S+E+W)

    orderDate_label = Label(rental_window, text = "order date")
    orderDate_label.grid(row = 3, column = 0, sticky=N+S+E+W)

    custID_label = Label(rental_window, text = "custID")
    custID_label.grid(row = 4, column = 0, sticky=N+S+E+W)

    vehicleID_label = Label(rental_window, text = "vehicleID")
    vehicleID_label.grid(row = 5, column = 0, sticky=N+S+E+W)

    rentalType_label = Label(rental_window, text = "rental type")
    rentalType_label.grid(row = 6, column = 0, sticky=N+S+E+W)

    qty_label = Label(rental_window, text = "qty")
    qty_label.grid(row = 7, column = 0, sticky=N+S+E+W)

    paymentDate_label = Label(rental_window, text = "payment date")
    paymentDate_label.grid(row = 8, column = 0, sticky=N+S+E+W)

    # define text boxes
    startDate = Entry(rental_window, width = 30)
    startDate.grid(row = 1, column = 1, padx = 20)

    returnDate = Entry(rental_window, width = 30)
    returnDate.grid(row = 2, column = 1, padx = 20)

    orderDate = Entry(rental_window, width = 30)
    orderDate.grid(row = 3, column = 1, padx = 20)

    custID = Entry(rental_window, width = 30)
    custID.grid(row = 4, column = 1, padx = 20)

    vehicleID = Entry(rental_window, width = 30)
    vehicleID.grid(row = 5, column = 1, padx = 20)

    rentalType = Entry(rental_window, width = 30)
    rentalType.grid(row = 6, column = 1, padx = 20)

    qty = Entry(rental_window, width = 30)
    qty.grid(row = 7, column = 1, padx = 20)

    paymentDate = Entry(rental_window, width = 30)
    paymentDate.grid(row = 8, column = 1, padx = 20)

    # Vehicle submit button
    submit_button = Button(rental_window, text = "add rental into the db", command = lambda: submitRental(
                                custID.get(), vehicleID.get(), startDate.get(), orderDate.get(), rentalType.get(),
                                qty.get(), returnDate.get(), paymentDate.get()))
    submit_button.grid(row = 9, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

    findAvailable_button = Button(rental_window, text = "find available vehicles in date range", 
                                            command = lambda: findAvailable(startDate.get(), orderDate.get()))
    findAvailable_button.grid(row = 10, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)
    
    info_label = Label(rental_window, text = "Add rental into database by inputing CustomerID as 'XXX', VehcicleID as 'XXXXXXXXXXXXXXXXX', "
                                            "start date as 'YYYY-MM-DD', order date as 'YYYY-MM-DD', rental type as 'X' (1 or 7), "
                                            "quantity as 'X', return date as 'YYYY-MM-DD', and payment date as 'YYYY-MM-DD' or 'NULL'"
                                            , font = ("ariel", 8))
    info_label.grid(row = 11, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)



# Function to update a return (pay for it)
def updateReturn(name, vehicleID, returnDate):
    return_conn = sqlite3.connect("CarRental.db")
    return_cur = return_conn.cursor()

    if (bool(re.match(name_re, name)) and bool(re.match(date_re, returnDate) )
        and bool(re.match(VIN_re, vehicleID))):
        return_cur.execute(f"UPDATE RENTAL SET PaymentDate = '{returnDate}', Returned = 1 "
                           f"WHERE VehicleID = '{vehicleID}' AND CustID = (SELECT CustID FROM Customer WHERE name LIKE '%{name}%')")
        return_cur.execute(f"SELECT TotalAmount an AmountPayed FROM RENTAL "
                           f"WHERE VehicleID = '{vehicleID}' AND CustID = (SELECT CustID FROM Customer WHERE name LIKE '%{name}%')")  
    
    records = return_cur.fetchall()
    columns = return_cur.description
    printToConsoleWithMoney(records,columns)

    # commits any changes to the db if any other connections are open
    return_conn.commit()
    return_conn.close()

# Function to display a window allowing for the update of a rental
def returnWindow():
    return_window = Toplevel(root_window)
    return_window.title("Return Vehicle")
    return_window.geometry("450x175")
    return_window.rowconfigure(0,weight=1)
    return_window.columnconfigure(0,weight=1)

    return_label = Label(return_window, text = "Return Screen", font = ("ariel", 15))
    return_label.grid(row = 0, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

    name_label = Label(return_window, text = "name")
    name_label.grid(row = 1, column = 0, sticky=N+S+E+W)

    vehicleID_label = Label(return_window, text = "vehicleID")
    vehicleID_label.grid(row = 2, column = 0, sticky=N+S+E+W)

    returnDate_label = Label(return_window, text = "return date")
    returnDate_label.grid(row = 3, column = 0, sticky=N+S+E+W)

    name = Entry(return_window, width = 30)
    name.grid(row = 1, column = 1, padx = 20)

    vehicleID = Entry(return_window, width = 30)
    vehicleID.grid(row = 2, column = 1, padx = 20)

    returnDate = Entry(return_window, width = 30)
    returnDate.grid(row = 3, column = 1, padx = 20)

    submit_button = Button(return_window, text = "Update rental in the db", command = lambda: updateReturn(
                                name.get(), vehicleID.get(), returnDate.get()))
    submit_button.grid(row = 4, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

    info_label = Label(return_window, text = "To return a car, insert customer name, vehicleID as 'XXXXXXXXXXXXXXXXX', "
                                            "and return date as 'YYYY-MM-DD'."
                                            , font = ("ariel", 8))
    info_label.grid(row = 5, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)



# Function to create the window utilized in accesing the custom view for customers
def custViewWindow():
    custView_window = Toplevel(root_window)
    custView_window.title("Customer View Search")
    custView_window.geometry("450x150")
    custView_window.rowconfigure(0,weight=1)
    custView_window.columnconfigure(0,weight=1)

    custView_label = Label(custView_window, text = "Customer View Screen", font = ("ariel", 15))
    custView_label.grid(row = 0, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

    # define labels
    customerID_label = Label(custView_window, text = "CustomerID")
    customerID_label.grid(row = 1, column = 0, sticky=N+S+E+W)

    name_label = Label(custView_window, text = "name")
    name_label.grid(row = 2, column = 0, sticky=N+S+E+W)

    # define Entry
    customerID = Entry(custView_window, width = 30)
    customerID.grid(row = 1, column = 1, padx = 20)

    name = Entry(custView_window, width = 30)
    name.grid(row = 2, column = 1, padx = 20)

    # Vehicle query button
    query_button = Button(custView_window, text = "show remaining balance", command = lambda: custViewQuery(customerID.get(), name.get()))
    query_button.grid(row = 5, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

    info_label = Label(custView_window, text = "To display all remaining balances, do not enter any paramaters, to search, "
                                                "input customers ID as 'XXX' and/or part of their name."
                                            , font = ("ariel", 8))
    info_label.grid(row = 6, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

# Prints search results to the console
def custViewQuery(customerID, name):
    custView_conn = sqlite3.connect("CarRental.db")
    custView_cur = custView_conn.cursor()
    
    if(name == '' and customerID == ''):
        custView_cur.execute(f"SELECT CustomerID, CustomerName, ROUND(SUM(CAST(RentalBalance AS Float)),2) AS RemainingBalance "
                              "FROM vRentalInfo GROUP BY CustomerID ORDER BY RemainingBalance")
    elif(name == '' and bool(re.match(custID_re, customerID))):
        print(customerID)
        custView_cur.execute(f"SELECT CustomerID, CustomerName, ROUND(SUM(CAST(RentalBalance AS Float)),2) AS RemainingBalance "
                             f"FROM vRentalInfo WHERE CustomerID = '{customerID}' GROUP BY CustomerID")
    elif(bool(re.match(name_re, name))):
        custView_cur.execute(f"SELECT CustomerID, CustomerName, ROUND(SUM(CAST(RentalBalance AS Float)),2) AS RemainingBalance "
                             f"FROM vRentalInfo WHERE CustomerName LIKE '%{name}%' GROUP BY CustomerID")
    elif(bool(re.match(name_re, name)) and bool(re.match(custID_re, customerID))):
        custView_cur.execute(f"SELECT CustomerID, CustomerName, ROUND(SUM(CAST(RentalBalance AS Float)),2) AS Remaining Balance "
                              "FROM vRentalInfo GROUP BY CustomerID"
                             f"WHERE CustomerID = '{customerID} AND CustomerName LIKE '%{name}%' GROUP BY CustomerID")
    
    records = custView_cur.fetchall()
    columns = custView_cur.description

    

    printToConsoleWithMoney(records, columns)



# Function to create the window utilized in accesing the custom view for vehicles
def carViewWindow():
    carView_window = Toplevel(root_window)
    carView_window.title("Vehicle View Search")
    carView_window.geometry("450x150")
    carView_window.rowconfigure(0,weight=1)
    carView_window.columnconfigure(0,weight=1)

    carView_label = Label(carView_window, text = "Car View Screen", font = ("ariel", 15))
    carView_label.grid(row = 0, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W) 

    # define labels
    vin_label = Label(carView_window, text = "vin")
    vin_label.grid(row = 1, column = 0, sticky=N+S+E+W)

    vehicle = Label(carView_window, text = "Vehicle")
    vehicle.grid(row = 2, column = 0, sticky=N+S+E+W)\

    # define Entrys
    vin = Entry(carView_window, width = 30)
    vin.grid(row = 1, column = 1, padx = 20)

    vehicle = Entry(carView_window, width = 30)
    vehicle.grid(row = 2, column = 1, padx = 20)

    # Vehicle query button
    query_button = Button(carView_window, text = "Show average daily rates", command = lambda: carViewQuery(vin.get(), vehicle.get()))
    query_button.grid(row = 3, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

    info_label = Label(carView_window, text = "To display all daily rate averages, do not enter any paramaters, to search, "
                                                "input VehicleID as 'XXXXXXXXXXXXXXXXX' and/or part of their description."
                                            , font = ("ariel", 8))
    info_label.grid(row = 6, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

# Prints search results to the console
def carViewQuery(vin, vehicle):
    carView_conn = sqlite3.connect("CarRental.db")
    carView_cur = carView_conn.cursor()
    
    if(vin == '' and vehicle == ''):
        carView_cur.execute(f"SELECT VIN, vehicle, ROUND((SUM(CAST(OrderAmount AS float))/SUM(TotalDays)),2) AS AverageDailyPrice "
                             "FROM vRentalInfo GROUP BY VIN ORDER BY AverageDailyPrice")
    elif(vin == '' and bool(re.match(desc_re, vehicle))):
        carView_cur.execute(f"SELECT VIN, vehicle, ROUND((SUM(CAST(OrderAmount AS float))/SUM(TotalDays)),2) AS AverageDailyPrice "
                            f"FROM vRentalInfo WHERE vehicle LIKE '%{vehicle}%' GROUP BY VIN")
    elif(bool(re.match(VIN_re, vin)) and vehicle == ''):
        carView_cur.execute(f"SELECT VIN, vehicle, ROUND((SUM(CAST(OrderAmount AS float))/SUM(TotalDays)),2) AS AverageDailyPrice "
                            f"FROM vRentalInfo WHERE VIN = '{vin}' GROUP BY VIN")
    elif(bool(re.match(VIN_re, vin)) and bool(re.match(desc_re, vehicle))):
        carView_cur.execute(f"SELECT VIN, vehicle, ROUND((SUM(CAST(OrderAmount AS float))/SUM(TotalDays)),2) AS AverageDailyPrice "
                            f"FROM vRentalInfo WHERE VIN = '{vin}'' AND vehicle LIKE '%{vehicle}%' GROUP BY VIN")
    
    records = carView_cur.fetchall()
    columns = carView_cur.description

    

    printToConsoleWithMoney(records, columns)



# Window label
root_label = Label(root_window, text = "Hub Screen", font = ("ariel", 15))
root_label.grid(row = 0, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

# define GUI components for tkinter root window
goto_custy = Button(root_window, text = "Add a new customer", command = custyWindow)
goto_custy.grid(row = 1, column = 0, columnspan = 1, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

# custy querry button
query_custy_button = Button(root_window, text = "show all customers", command = custy_query)
query_custy_button.grid(row = 1, column = 1, columnspan = 1, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

goto_vehicle = Button(root_window, text = "Add a new vehicle", command = vehicleWindow)
goto_vehicle.grid(row = 2, column = 0, columnspan = 1, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

# Vehicle query button
vehicle_query_button = Button(root_window, text = "show all vehicles", command = vehicle_query)
vehicle_query_button.grid(row = 2, column = 1, columnspan = 1, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

goto_rental = Button(root_window, text = "Add a new rental", command = rentalWindow)
goto_rental.grid(row = 3, column = 0, columnspan = 1, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

# Rental query button
rental_query_button = Button(root_window, text = "show all rentals", command = rental_query)
rental_query_button.grid(row = 3, column = 1, columnspan = 1, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

goto_return = Button(root_window, text = "Return a car", command = returnWindow)
goto_return.grid(row = 4, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

goto_custViewWindow = Button(root_window, text = "Get remaining balance for customers", command = custViewWindow)
goto_custViewWindow.grid(row = 5, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

goto_carViewWindow = Button(root_window, text = "Get average daily price for vehicles", command = carViewWindow)
goto_carViewWindow.grid(row = 6, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

# Real console
console = Listbox(root_window, bg='black', fg='white', font = 'courier', bd = 20, height = 30)
console.grid(row = 7, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100, sticky=N+S+E+W)

# exectutes window
root_window.mainloop()
