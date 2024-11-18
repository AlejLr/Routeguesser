import Map
from Flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MIN_DISTANCE = 5

@app.route('/main', methods=['POST'])
def main():
    """
    processes the inputs from the webpage
    """
    data = request.get_json()
    if data["type"] == "start":
        return send_start(data)
    elif data["type"] == "neighbours":
        return send_neighbours(data)
 
    
    return jsonify({"error" : "The data is not a JSON or the format is invalid"}), 400

def send_start(data):
    """
    sends the start, end and blocked nodes to the UI in a JSON file
    """

    map = Map("complex_graph.json")
    data["difficulty"] = map.difficulty
    blocked_roads = map.get_blocked_roads_list()
    neighbours = map.get_neighbours_and_roads()
    return jsonify({"start" : map.start, "end" : map.end, "blocked nodes": blocked_roads, "neighbours": neighbours, "optimal path" :  map.optimal_path, "optimal distance" : map.optimal_distance})

def send_neighbours(data):
    """
    calls generate neighbours and sends to the UI a JSON file with them
    """
    
    neighbours = map.get_neighbours_and_roads()
    map.process_inputs(data["current"])
    return jsonify({neighbours})

if __name__ == "__main__":
    while True:
        app.run(debug=True)
        data = request.get_json()
        if data["type"] == "end":
            break

# testing if some functions work properly
# Graph = gr.GeoGraph("map_complex.geojson")
# print(Graph.G.nodes)
# Map = Map.Map(Graph)
# print(Map.generate_start_end(1000))
