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
    elif data["type"] == "end":
        return send_score_and_path(data)
    
    return jsonify({"error" : "The data is not a JSON or the format is invalid"}), 400

def send_start(data):
    """
    sends the start, end and blocked nodes to the UI in a JSON file
    """
    map = Map("complex_graph.json")
    data["difficulty"] = map.difficulty
    startend = map.startend
    blocked_nodes = map.generate_blocked_nodes()
    neighbours = map.generate_neighbours(5)
    optimal_paths = map.optimal_path
    return jsonify({"startend" : startend, "blocked nodes": blocked_nodes, "neighbours": neighbours, "optimal path" :  optimal_paths})

def send_neighbours(data):
    """
    calls generate neighbours and sends to the UI a JSON file with them
    """
    
    neighbours = map.generate_neighbours(MIN_DISTANCE)
    map.process_inputs(data["current"])
    return jsonify({"neighbours": neighbours})

def send_score_and_path(data):
    """
    sends the score to the UI in a JSON file
    """
    map.process_inputs(data["current"])
    return jsonify({"paths": optimal_paths})


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
