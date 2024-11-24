from Map import Map
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


def send_start(data):
    """
    sends the start, end and blocked nodes to the UI in a JSON file
    """
    # Quick and messy handling 
    map = Map("complex_graph.json", data["type"], data["difficulty"])
    neighbours = map.get_neighbours_and_roads(map.current_pos)
    neighbours_str_keys = {str(k): v for k, v in neighbours.items()}
    
    return jsonify({"start" : map.start, 
                    "end" : map.end, 
                    "blocked nodes": map.blocked_roads, 
                    "neighbours": neighbours_str_keys, #self.map.get_neighbours_and_roads(self.map.current_pos), 
                    "optimal path" :  map.optimal_path, 
                    "optimal distance" : map.optimal_distance})

def send_neighbours(data):
    """
    calls generate neighbours and sends to the UI a JSON file with them
    """
    map = Map("complex_graph.json", data["type"])
    neighbours = map.get_neighbours_and_roads(data["current"])
    neighbours_str_keys = {str(k): v for k, v in neighbours.items()}
    return jsonify({{"neighbours": neighbours_str_keys}})


@app.route('/main', methods=['POST'])
def main():
    """
    processes the inputs from the webpage
    """
    data = request.get_json()
    
    print("Received data:", data)  # Debugging :)
    
    if data["type"] == "start":
        # initialize the map object and return the starting information for the frontend
        return send_start(data)
    elif data["type"] == "neighbours":
        return send_neighbours(data)
 
    
    return jsonify({"error" : "The data is not a JSON or the format is invalid"}), 400


if __name__ == "__main__":
    app.run(debug=True)

# testing if some functions work properly
# Graph = gr.GeoGraph("map_complex.geojson")
# print(Graph.G.nodes)
# Map = Map.Map(Graph)
# print(Map.generate_start_end(1000))
