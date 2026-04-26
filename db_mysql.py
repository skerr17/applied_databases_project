# program used to connect to mysql database and execute queries

import mysql.connector
from config import mysql_config

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