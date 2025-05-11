import csv
import random

# File đã chứa các cạnh và khoảng cách
input_edge_csv_path = "Data/district7_edges.csv"
output_augmented_csv_path = "Data/district7_edges_augmented.csv"

# Hàm xếp hạng travel_time từ khoảng cách (1 - 10)
def estimate_travel_time(distance):
    # Giả định: dưới 100m => 1, trên 500m => 10, tuyến tính nội suy
    return min(10, max(1, int((distance / 500) * 10)))

# Hàm gán nhãn traffic_density ngẫu nhiên theo phân bố xác suất
def simulate_traffic_density():
    return random.choices(
        population=["low", "medium", "high"],
        weights=[0.5, 0.3, 0.2],  # Ước lượng xác suất
        k=1
    )[0]

# Đọc file cạnh, ghi file mới có thêm 2 cột
with open(input_edge_csv_path, mode="r", encoding="utf-8") as infile, \
     open(output_augmented_csv_path, mode="w", newline='', encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["Travel Time (1-10)", "Traffic Density"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        distance = float(row["Distance (m)"])
        row["Travel Time (1-10)"] = estimate_travel_time(distance)
        row["Traffic Density"] = simulate_traffic_density()
        writer.writerow(row)

output_augmented_csv_path
