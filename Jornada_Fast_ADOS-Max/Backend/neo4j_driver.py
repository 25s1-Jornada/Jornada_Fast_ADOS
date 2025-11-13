from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session(database=os.getenv("NEO4J_DB_NAME")) as session:
    result = session.run("MATCH (n) RETURN COUNT(n) AS nodes")
    print(result.single())
