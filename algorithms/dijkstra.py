import heapq

# def calculate_edge_weight(edge, use_time=False, use_traffic=False):
#     """
#     Calculate weight based on:
#     - always use distance
#     - optionally include travel_time and traffic_density
#     """
#     weight = edge["distance"]

#     if use_time and "travel_time" in edge:
#         time_weight = edge["travel_time"]

#         if use_traffic and "traffic_density" in edge:
#             traffic_factors = {"low": 1.0, "medium": 1.2, "high": 1.5}
#             factor = traffic_factors.get(edge["traffic_density"], 1.0)
#             time_weight *= factor

#         weight += time_weight

#     return weight

def calculate_edge_weight(edge, use_time=False, use_traffic=False):
    """
    Tổng hợp chi phí cạnh từ nhiều yếu tố:
    - distance: bắt buộc
    - travel_time: optional
    - traffic_density: optional

    Trọng số đề xuất:
        - distance (p1): 0.5
        - time (p2): 0.1
        - surface/traffic (p3): 0.4
    """
    weight = 0
    p1, p2, p3 = 0.5, 0.1, 0.4

    # Base distance (must-have)
    weight += p1 * edge["distance"]

    # Optional: travel_time (if available)
    if use_time and "travel_time" in edge:
        weight += p2 * edge["travel_time"]

    # Optional: traffic or surface
    if use_traffic and "traffic_density" in edge:
        traffic_factor = {"low": 1.0, "medium": 1.2, "high": 1.5}
        factor = traffic_factor.get(edge["traffic_density"], 1.0)
        weight += p3 * factor
        
    return weight



def dijkstra(nodes, edges, source, target=None, use_time=False, use_traffic=False):
    """
    Dijkstra's algorithm with flexible edge weights
    """
    distances = {node: float('inf') for node in nodes}
    distances[source] = 0
    previous_nodes = {node: None for node in nodes}
    pq = [(0, source)]

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node == target:
            break

        for (start, end), edge in edges.items():
            if start == current_node:
                if edge.get("one_way", False) and current_node != start:
                    continue

                weight = calculate_edge_weight(edge, use_time, use_traffic)
                new_distance = current_distance + weight

                if new_distance < distances[end]:
                    distances[end] = new_distance
                    previous_nodes[end] = current_node
                    heapq.heappush(pq, (new_distance, end))

    return distances, previous_nodes


def reconstruct_path(previous_nodes, source, target):
    path = []
    current = target
    while current != source:
        if current is None:
            return None
        path.append(current)
        current = previous_nodes[current]
    path.append(source)
    return path[::-1]



