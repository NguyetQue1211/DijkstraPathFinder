import csv
import math
import random

# Đường dẫn đến file CSV chứa thông tin các địa điểm
input_csv_path = "Data/district7_data.csv"
output_edge_csv_path = "Data/district7_edges.csv"
output_mst_csv_path = "Data/district7_mst_edges.csv"  # Output file for MST

# Bán kính xác định adjacency
radius_meters = 2000
R = 6371000  # Bán kính Trái Đất theo mét

# Hàm tính khoảng cách giữa 2 điểm bằng công thức Haversine
def haversine(coord1, coord2, radius=R, verbose=False):
    try:
        lat1, lon1 = map(float, coord1)
        lat2, lon2 = map(float, coord2)
    except (TypeError, ValueError):
        raise ValueError("Input coordinates must be numeric and in (lat, lon) format.")

    # Đổi độ sang radian
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Áp dụng công thức Haversine
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    if verbose:
        print(f"Distance from {coord1} to {coord2}: {distance:.2f} meters")

    return round(distance, 2)

# Đọc dữ liệu từ CSV
locations = []
with open(input_csv_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row["Name"]
        lat = float(row["Latitude"])
        lon = float(row["Longitude"])
        locations.append((name, lat, lon))

# Tính adjacency dựa trên bán kính và lưu vào danh sách các edges
edges = []
for i, (name_i, lat_i, lon_i) in enumerate(locations):
    for j, (name_j, lat_j, lon_j) in enumerate(locations):
        if i != j:
            dist = haversine((lat_i, lon_i), (lat_j, lon_j))
            if dist <= radius_meters:
                edges.append((name_i, name_j, dist))

# Hàm tìm kiếm theo nhóm (Union-Find)
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1

# Kruskal’s algorithm để xây dựng cây khung (MST)
def kruskal(nodes, edges):
    uf = UnionFind(len(nodes))
    mst = []  # Minimum Spanning Tree
    edges.sort(key=lambda x: x[2])  # Sắp xếp edges theo trọng số (distance)
    
    for edge in edges:
        node1, node2, distance = edge
        idx1 = list(nodes.keys()).index(node1)
        idx2 = list(nodes.keys()).index(node2)
        
        if uf.find(idx1) != uf.find(idx2):
            uf.union(idx1, idx2)
            mst.append((node1, node2, distance))  # Thêm vào cây khung
    
    return mst

# Tạo cây khung (MST) từ các edges đã tạo
nodes = {location[0]: location[1:] for location in locations}  # Tạo dictionary nodes
mst = kruskal(nodes, edges)

# Thêm các edges ngẫu nhiên để làm tăng mật độ đồ thị
random_edges = []
for i in range(100):  # Limit the number of random edges added
    if random.random() < 0.3:  # 30% chance to add an edge
        random_pair = random.choice(edges)  # Random edge
        random_edges.append(random_pair)

# Kết hợp MST và random edges
edges += random_edges

# Ghi các cạnh của cây khung vào file CSV
with open(output_mst_csv_path, mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["From", "To", "Distance (m)"])
    for edge in mst:
        writer.writerow(edge)

# Ghi danh sách các edges vào file CSV
with open(output_edge_csv_path, mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["From", "To", "Distance (m)"])
    for edge in edges:
        writer.writerow(edge)

# In ra kết quả cây khung
print(f"Minimum Spanning Tree saved to {output_mst_csv_path}")
print(f"Edges (with extra random edges) saved to {output_edge_csv_path}")
