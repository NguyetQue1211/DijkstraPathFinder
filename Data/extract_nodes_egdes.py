import csv
import networkx as nx

# File paths
nodes_csv_path = "Data/district7_data.csv"
edges_csv_path = "Data/district7_edges_augmented.csv"

# Parse nodes
nodes = {}
with open(nodes_csv_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for idx, row in enumerate(reader, 1):
        name = row["Name"]
        lat = float(row["Latitude"])
        lon = float(row["Longitude"])
        nodes[name] = {"id": idx, "coordinates": (lat, lon)}

# Parse edges
edges = {}
with open(edges_csv_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        start = row["From"]
        end = row["To"]
        distance = float(row["Distance (m)"])
        travel_time = int(row["Travel Time (1-10)"])
        traffic_density = row["Traffic Density"]
        edges[(start, end)] = {
            "distance": distance,
            "travel_time": travel_time,
            "traffic_density": traffic_density,
            "one_way": False  # always False as requested
        }

nodes, edges


# Initialize NetworkX graph
G = nx.Graph()

# Add nodes to the graph
for node, coords in nodes.items():
    G.add_node(node, coordinates=coords)

# Add edges to the graph
for (node1, node2), edge_data in edges.items():
    G.add_edge(node1, node2, **edge_data)

