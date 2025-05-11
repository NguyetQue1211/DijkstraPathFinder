import networkx as nx
from extract_nodes_egdes import nodes, edges

# Initialize NetworkX graph
G = nx.Graph()

# Add nodes to the graph
for node, coords in nodes.items():
    G.add_node(node, coordinates=coords)

# Add edges to the graph
for (node1, node2), edge_data in edges.items():
    G.add_edge(node1, node2, **edge_data)
    

source = "15-27-Block M2-Sảnh B, Jamona City, Đào Trí,"
target = "67 Mai Văn Vĩnh,"

shortest_path = nx.shortest_path(G, source=source, target=target, weight='distance')

print(f"According to networkx, shortest path: {shortest_path}")
