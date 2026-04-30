# program used to connect to mysql database and execute queries
# Author: Stephen Kerr


import mysql.connector
from config import mysql_config


# function to connect to mysql database and return the connection object
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host=mysql_config['host'],
            user=mysql_config['user'],
            password=mysql_config['password'],
            database=mysql_config['database']
        )
        print("Connected to MySQL database")
        return connection
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
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
        print(f"Error: {err}")
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
        print(f"Error: {err}")
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
        print(f"Error: {err}")
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
        print(f"Error: {err}")
        return []