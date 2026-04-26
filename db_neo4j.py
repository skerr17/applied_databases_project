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
