from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

class Neo4jConnection:
    def __init__(self):
        self._driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(
                os.getenv("NEO4J_USER"),
                os.getenv("NEO4J_PASSWORD")
            )
        )

    def close(self):
        self._driver.close()

    def query(self, query: str, parameters: dict = None):
        with self._driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]


# Instância global (evita reconectar toda hora)
neo4j_db = Neo4jConnection()
