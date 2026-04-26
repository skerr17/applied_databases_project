# main prgram of the project, which will run the whole program

from db_mysql import connect_to_mysql
from db_neo4j import connect_to_neo4j

def main():
    # Connect to MySQL database
    mysql_connection = connect_to_mysql()
    
    # Connect to Neo4j database
    neo4j_driver = connect_to_neo4j()
    
    # Here you can add code to execute queries on both databases and perform operations
    
    # Close the connections
    if mysql_connection:
        mysql_connection.close()
        print("MySQL connection closed")
    
    if neo4j_driver:
        neo4j_driver.close()
        print("Neo4j connection closed")

if __name__ == "__main__":
    main()
    
