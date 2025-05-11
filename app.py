from flask import Flask, render_template, request, jsonify
import json
from algorithms.dijkstra import dijkstra, calculate_edge_weight, reconstruct_path
from Data.extract_nodes_egdes import nodes, edges


app = Flask(__name__)

# Convert edges to use string keys instead of tuples for JSON serialization
edges_str_keys = {
    f"{start}-{end}": {
        "distance": edge["distance"],
        "travel_time": edge["travel_time"],
        "traffic_density": edge["traffic_density"],
        "one_way": edge["one_way"]
    }
    for (start, end), edge in edges.items()
}

@app.route('/')
def index():
    # Render the index page with nodes and edges
    return render_template('index.html', nodes=nodes, edges=edges_str_keys)


@app.route('/get_nodes', methods=['GET'])
def get_nodes():
    # Convert nodes dictionary to a list of objects with id and name
    nodes_list = [{"id": node_data["id"], "name": node_name} for node_name, node_data in nodes.items()]
    return jsonify(nodes_list)

@app.route('/find_shortest_path', methods=['POST'])
def find_shortest_path():
    source = request.form.get('source')
    target = request.form.get('target')
    consider_traffic_time = request.form.get('consider_traffic_time') == 'true'
    consider_traffic_density = request.form.get('consider_traffic_density') == 'true'

    print(f"Source: {source}, Target: {target}, Traffic Time: {consider_traffic_time}, Traffic Density: {consider_traffic_density}")  # Debugging

    # Ensure source and target are valid
    if source not in nodes or target not in nodes:
        return jsonify({"error": "Invalid source or target"}), 400

    # Calculate shortest path using Dijkstra's algorithm
    try:
        distances, previous_nodes = dijkstra(nodes, edges, source, consider_traffic_time, consider_traffic_density)
        path = reconstruct_path(previous_nodes, source, target)

        # Return the result as JSON
        return jsonify({
            
            "path": path,
            "distance": distances[target],
            # "estimated_time": distances[target] / 50,  # Example: Assume 50 m/s speed
            # "traffic_status": "Moderate"  # Example: Add traffic status if needed
        })
    except Exception as e:
        print(f"Error calculating shortest path: {e}")
        return jsonify({"error": "Failed to calculate shortest path"}), 500

if __name__ == '__main__':
    app.run(debug=True)