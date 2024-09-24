from orionsdk import SwisClient
import requests

class SolarWindsAPI:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.swis = None

    def connect(self):
        try:
            self.swis = SwisClient(self.hostname, self.username, self.password)
            print("Connection successful!")
        except Exception as e:
            print(f"Error connecting: {e}")

    def query_nodes(self, top_n=5):
        query = f"SELECT TOP {top_n} NodeID, IPAddress, Caption FROM Orion.Nodes"
        try:
            result = self.swis.query(query)
            for node in result['results']:
                print(f"NodeID: {node['NodeID']}, IPAddress: {node['IPAddress']}, Caption: {node['Caption']}")
        except Exception as e:
            print(f"Query failed: {e}")

    def add_router(self, node_details):
        try:
            node_uri = self.swis.create('Orion.Nodes', **node_details)
            print(f"Node created with URI: {node_uri}")
        except Exception as e:
            print(f"Error adding router: {e}")

    def find_node_by_ip(self, ip_address):
        try:
            query = f"SELECT NodeID, Caption FROM Orion.Nodes WHERE IPAddress = '{ip_address}'"
            result = self.swis.query(query)
            if result['results']:
                node_id = result['results'][0]['NodeID']
                caption = result['results'][0]['Caption']
                print(f"Node found: NodeID = {node_id}, Caption = {caption}")
                return node_id
            else:
                print(f"No node found with IP {ip_address}.")
                return None
        except Exception as e:
            print(f"Error querying node by IP: {e}")
            return None

    def delete_router(self, node_id):
        try:
            node_uri = f"swis://Orion/Orion.Nodes/NodeID={node_id}"
            self.swis.delete(node_uri)
            print(f"Node with NodeID {node_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting node: {e}")

if __name__ == "__main__":
    hostname = "192.168.1.100"
    username = "your_username"
    password = "your_password"

    solarwinds_api = SolarWindsAPI(hostname, username, password)
    solarwinds_api.connect()
    solarwinds_api.query_nodes()

    node_details = {
        'Caption': 'Router_Name',
        'IPAddress': '192.168.1.1',
        'EngineID': 1,
        'ObjectSubType': 'SNMP',
        'SNMPVersion': 2,
        'Community': 'public'
    }
    solarwinds_api.add_router(node_details)

    ip_address = '192.168.1.1'
    node_id = solarwinds_api.find_node_by_ip(ip_address)

    if node_id:
        solarwinds_api.delete_router(node_id)
