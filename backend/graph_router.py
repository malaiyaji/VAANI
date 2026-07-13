import os
from neo4j import GraphDatabase

NEO4J_URI = os.environ.get("NEO4J_URI", "neo4j+s://d4c69ff1.databases.neo4j.io")
NEO4J_USER = os.environ.get("NEO4J_USER", "d4c69ff1")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "vTquqhn4OgVBlGtdYgPfuAxETh_ZYZ5M9CrdkM1esGg")

class VAANIGraphRouter:
    def __init__(self):
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
            self.driver.verify_connectivity()
            self.online = True
            print("[GRAPH DB] Connected successfully to Aura Node.")
        except Exception as e:
            self.online = False
            print(f"[GRAPH DB WARNING] Connection failed: {e}. Defaulting to Offline Engine Mode.")

    def close(self):
        if self.driver:
            self.driver.close()

    def bootstrap_database(self):
        """Initializes default mock resources and architectural sectors in the graph."""
        if not self.online:
            return
            
        query = """
        MERGE (s1:Sector {id: "SECTOR_E4", name: "Sector E4 (Industrial Grid)"})
        MERGE (s2:Sector {id: "FLOOR_03", name: "Floor 03 (Server Complex)"})
        
        MERGE (r1:Resource {id: "R_DRONE_01", name: "DRONE_SURVEILLANCE_GRID_E4", type: "Surveillance"})
        MERGE (r2:Resource {id: "R_HAZMAT_03", name: "HAZMAT_CONTAINMENT_ECHELON_3", type: "Hazmat"})
        MERGE (r3:Resource {id: "R_RESCUE_OMEGA", name: "RESCUE_SQUAD_OMEGA", type: "Rescue"})
        
        MERGE (r1)-[:STATIONED_IN]->(s1)
        MERGE (r2)-[:STATIONED_IN]->(s2)
        MERGE (r3)-[:STATIONED_IN]->(s1)
        """
        try:
            with self.driver.session() as session:
                session.run(query)
                print("[GRAPH DB] Core pipeline nodes bootstrapped and linked successfully.")
        except Exception as e:
            print(f"[GRAPH DB ERROR] Bootstrapping failed: {e}")

    def find_and_link_dispatch(self, job_id, incident_type, sector_id):
        """Creates an Incident node and maps the closest available matching resource asset."""
        if not self.online:
            import random
            return random.choice([
                "ALPHA_STRIKE_UNIT_01 (SPATIAL)",
                "DRONE_SURVEILLANCE_GRID_E4",
                "RESCUE_SQUAD_OMEGA"
            ])

        query = """
        MATCH (s:Sector {id: $sector_id})
        MERGE (i:Incident {id: $job_id, type: $incident_type, status: "ACTIVE"})
        MERGE (i)-[:OCCURRED_IN]->(s)
        WITH s, i
        MATCH (r:Resource)-[:STATIONED_IN]->(s)
        WHERE NOT (r)-[:ASSIGNED_TO]->(:Incident {status: "ACTIVE"})
        MERGE (r)-[:ASSIGNED_TO]->(i)
        RETURN r.name AS allocated_resource
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, job_id=job_id, incident_type=incident_type, sector_id=sector_id)
                record = result.single()
                if record and record["allocated_resource"]:
                    return record["allocated_resource"]
                return "ALPHA_STRIKE_UNIT_01 (SPATIAL)"
        except Exception as e:
            print(f"[GRAPH RUNTIME ERROR] Match query faulted: {e}")
            return "DEFAULT_LOGISTICS_SUPPORT_ROUTER_V4"