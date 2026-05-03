# program used to connect to mysql database and execute queries
# Author: Stephen Kerr


import mysql.connector
from config import mysql_config


from colorama import init, Fore, Style # for colored text in the terminal

init(autoreset=True) # initialize colorama

# function to connect to mysql database and return the connection object
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host=mysql_config['host'],
            user=mysql_config['user'],
            password=mysql_config['password'],
            database=mysql_config['database']
        )
        print(Fore.GREEN + "Connected to MySQL database")
        return connection
    
    except mysql.connector.Error as err:
        print(Fore.RED + f"Error: {err}")
        return None
    
# function to get all rooms from the database 
def get_rooms(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT roomID, roomName, capacity FROM room"
        cursor.execute(query)
        rooms = cursor.fetchall()
        return rooms
    
    except mysql.connector.Error as err:
        print(Fore.RED + f"Error: {err}")
        return []


# function to search for a speaker by name (or part of the name) and return their details
def search_speaker_by_name(connection, name):
    try:
        cursor = connection.cursor()
        query = """
        SELECT s.speakerName, s.sessionTitle, r.roomName
        FROM session s
        JOIN room r ON s.roomID = r.roomID
        WHERE s.speakerName LIKE %s;
        """
        cursor.execute(query, (f"%{name}%",))
        speakers = cursor.fetchall()
        return speakers
    
    except mysql.connector.Error as err:
        print(Fore.RED + f"Error: {err}")
        return []

# function to get a company
def get_company(connection, company_id):
    try:
        cursor = connection.cursor()
        query = "SELECT companyID, companyName FROM company WHERE companyID = %s"
        cursor.execute(query, (company_id,))
        company = cursor.fetchone()
        return company
    
    except mysql.connector.Error as err:
        print(Fore.RED + f"Error: {err}")
        return None


# function to get the attendees_by_company
def get_attendees_by_company(connection, company_id):
    try:
        cursor = connection.cursor()
        query = """
            SELECT a.attendeeName, a.attendeeDOB, s.sessionTitle, s.speakerName, r.roomName
            FROM attendee a
            JOIN registration reg ON a.attendeeID = reg.attendeeID
            JOIN session s ON reg.sessionID = s.sessionID
            JOIN room r on s.roomID = r.roomID
            WHERE a. attendeeCompanyID = %s;
        """
        cursor.execute(query, (company_id,))
        attendees = cursor.fetchall()
        return attendees
    
    except mysql.connector.Error as err:
        print(Fore.RED + f"Error: {err}")
        return []
    

# function to add an attendee to the database
def add_attendee(connection, attendee_id, name, dob, gender, company_id):

    cursor = connection.cursor()

    # check if attendee id already exists
    cursor.execute("SELECT attendeeID FROM attendee WHERE attendeeID = %s", (attendee_id,))
    if cursor.fetchone():
        print(Fore.RED + f"*** ERROR *** Attendee ID: {attendee_id} already exists.")
        return False
    
    # check if company id exists
    cursor.execute("SELECT companyID FROM company WHERE companyID = %s", (company_id,))
    if not cursor.fetchone():
        print(Fore.RED + f"*** ERROR *** Company ID: {company_id} does not exist.")
        return False
    
    # check gender is valid
    if gender not in ["Male", "Female"]:
        print(Fore.RED + f"*** ERROR *** Gender must be Male/Female.")
        return False
    

    try:
        query = "INSERT INTO attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (attendee_id, name, dob, gender, company_id))
        connection.commit()
        print(Fore.GREEN + "Attendee successfully added.")
        return True
    
    except mysql.connector.Error as err:
        print(Fore.RED + f"Error: {err}")




# function to get an attendee by ID returning their name
def get_attendee_by_id(connection, attendee_id):
    try:
        cursor = connection.cursor()
        query = "SELECT  attendeeName FROM attendee WHERE attendeeID = %s"
        cursor.execute(query, (attendee_id,))
        attendee = cursor.fetchone()
        return attendee
    
    except mysql.connector.Error as err:
        print(Fore.RED + f"Error: {err}")
        return None