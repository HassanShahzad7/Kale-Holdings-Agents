from rdflib import Graph, Namespace
from typing import Dict, List, Optional
import logging

class OWLReader:
    def __init__(self, owl_file_path: str):
        self.graph = Graph()
        try:
            self.graph.parse(owl_file_path, format="xml")
            self.ma = Namespace("http://www.marketing-agents.org/ontology#")
        except Exception as e:
            logging.error(f"Error loading OWL file: {e}")
            raise

    def get_agent_details(self, agent_name: str) -> Optional[Dict]:
        try:
            agent_uri = self.ma[agent_name]
            query = f"""
            SELECT ?property ?value
            WHERE {{
                ma:{agent_name} ?property ?value .
            }}
            """
            results = self.graph.query(query)
            
            if not results:
                return None
                
            agent_details = {
                "responsibilities": [],
                "tools": [],
                "delegates_to": [],
                "reports_to": [],
                "receives_from": []
            }
            
            for row in results:
                prop = str(row.property).split("#")[-1]
                value = str(row.value)
                
                if prop == "responsibility":
                    agent_details["responsibilities"].append(value)
                elif prop == "tools":
                    agent_details["tools"].append(value)
                elif prop == "delegates_to":
                    agent_details["delegates_to"].append(value)
                elif prop == "reports_to":
                    agent_details["reports_to"].append(value)
                elif prop == "receives_from":
                    agent_details["receives_from"].append(value)
                    
            return agent_details
            
        except Exception as e:
            logging.error(f"Error retrieving agent details: {e}")
            return None

    def get_reporting_chain(self) -> Dict[str, List[str]]:
        """Returns the reporting structure of agents"""
        chain = {}
        try:
            query = """
            SELECT ?agent ?reports_to
            WHERE {
                ?agent ma:reports_to ?reports_to .
            }
            """
            results = self.graph.query(query)
            for row in results:
                agent = str(row[0]).split("#")[-1]
                reports_to = str(row[1]).split("#")[-1]
                chain[agent] = reports_to
            return chain
        except Exception as e:
            logging.error(f"Error retrieving reporting chain: {e}")
            return {}

    def get_delegation_chain(self) -> Dict[str, List[str]]:
        """Returns delegation structure of agents"""
        chain = {}
        try:
            query = """
            SELECT ?agent ?delegates_to
            WHERE {
                ?agent ma:delegates_to ?delegates_to .
            }
            """
            results = self.graph.query(query)
            for row in results:
                agent = str(row[0]).split("#")[-1]
                if agent not in chain:
                    chain[agent] = []
                chain[agent].append(str(row[1]).split("#")[-1])
            return chain
        except Exception as e:
            logging.error(f"Error retrieving delegation chain: {e}")
            return {}