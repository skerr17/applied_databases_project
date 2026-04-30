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

