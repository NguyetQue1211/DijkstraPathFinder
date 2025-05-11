import overpy
import csv
import random

api = overpy.Overpass()

query = """
[out:json][timeout:25];
area["name"="Quận 7"]["boundary"="administrative"]->.searchArea;
(
  node["name"](area.searchArea);
);
out center;
"""

result = api.query(query)

selected_nodes = random.sample(result.nodes, min(100, len(result.nodes)))


with open("Data/district7_data.csv", mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Latitude", "Longitude"])
    for node in selected_nodes:
        name = node.tags.get("name", "Unknown")
        writer.writerow([name, node.lat, node.lon])
