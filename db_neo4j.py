# program to connect to neo4j database and execute queries
# Author: Stephen Kerr


from neo4j import GraphDatabase
from config import neo4j_config


from colorama import init, Fore, Style # for colored text in the terminal

init(autoreset=True) # initialize colorama


def connect_to_neo4j():
    try:
        driver = GraphDatabase.driver(
            neo4j_config['uri'],
            auth=(neo4j_config['user'], neo4j_config['password'])
        )
        print(Fore.GREEN + "Connected to Neo4j database")
        return driver
    
    except Exception as err:
        print(Fore.RED + f"Error: {err}")
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
        print(Fore.RED + f"Error: {err}")
        return []
    

# function to check if a connection exists between two attendees
def already_connected(driver, attendee_id1, attendee_id2):
    try:
        with driver.session() as session:
            query = """
            MATCH (a:Attendee {AttendeeID: $attendee_id1})-[:CONNECTED_TO]-(b:Attendee {AttendeeID: $attendee_id2})
            RETURN COUNT(*) AS count
            """
            result = session.run(query, attendee_id1=attendee_id1, attendee_id2=attendee_id2)
            count = result.single()["count"]
            return count > 0
    
    except Exception as err:
        print(Fore.RED + f"Error: {err}")
        return False

# function to add a connection between two attendees
def add_connection(driver, attendee_id1, attendee_id2):
    try:
        with driver.session() as session:
            query = """
            MERGE (a:Attendee {AttendeeID: $attendee_id1})
            MERGE (b:Attendee {AttendeeID: $attendee_id2})
            MERGE (a)-[:CONNECTED_TO]-(b)
            """
            session.run(query, attendee_id1=attendee_id1, attendee_id2=attendee_id2)
                
    except Exception as err:
        print(Fore.RED + f"Error: {err}")


# function to get the most connected attendee 
def get_most_connected(driver):
    try:
        with driver.session() as session:
            query = """
            MATCH (a:Attendee)-[:CONNECTED_TO]-(b:Attendee)
            RETURN a.AttendeeID AS ID, COUNT(b) AS Connections
            ORDER BY Connections DESC
            LIMIT 1
            """
            result = session.run(query)
            record = result.single()
            if record:
                return record["ID"], record["Connections"]
            else:
                return None
    
    except Exception as err:
        print(Fore.RED + f"Error: {err}")
        return None
    
# function to get friends of friends (2nd degree connections)
def get_friends_of_friends(driver, attendee_id, connected_attendees):
    try:
        friends_of_friends = {}
        with driver.session() as session:
            for cid in connected_attendees:
                query = """
                MATCH (a:Attendee {AttendeeID: $cid})-[:CONNECTED_TO]-(b:Attendee)
                WHERE b.AttendeeID <> $attendee_id AND NOT b.AttendeeID IN $connected_attendees
                RETURN b.AttendeeID AS ID
                """
                result = session.run(query, cid=cid, attendee_id=attendee_id, connected_attendees=connected_attendees)
                for record in result:
                    fof_id = [record["ID"] for record in result]
                    if fof_id:
                        friends_of_friends[cid] = fof_id
        return friends_of_friends
    except Exception as err:
        print(Fore.RED + f"Error: {err}")
        return {}

    