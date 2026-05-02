# program to connect to neo4j database and execute queries

from neo4j import GraphDatabase
from config import neo4j_config

def connect_to_neo4j():
    try:
        driver = GraphDatabase.driver(
            neo4j_config['uri'],
            auth=(neo4j_config['user'], neo4j_config['password'])
        )
        print("Connected to Neo4j database")
        return driver
    
    except Exception as err:
        print(f"Error: {err}")
        return None




# function to get all attendees connected to a given attendee
def get_connected_attendees(driver, attendee_id):
    try:
        with driver.session() as session:
            query = """
            MATCH (a:Attendee {AttendeeID: $attendee_id})-[:CONNECTED_TO]-(b:Attendee)
            RETURN b.AttendeeID AS ID
            """
            result = session.run(query, attendee_id=attendee_id)
            connected_attendees = [(record["ID"]) for record in result]
            return connected_attendees
    
    except Exception as err:
        print(f"Error: {err}")
        return []