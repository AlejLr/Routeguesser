from Map import Map
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# initialize the map object globally so that it can be used dynamically by the server, 
# when frontend sends requests with updated player position
# the second line is added for testing purposes and not needed for the actual server
if __name__ == "__main__":
    game = Map("map_graph.json")
else:
    game = Map("map_test_5-1.json")

def send_start(data: dict) -> dict:
    """
    sends the start, end and blocked nodes to the UI in a JSON file
    Keep tracks of the round to reset start and end when needed
    :rtype dict:
    """
    game.game_init(data["difficulty"])
    return jsonify({"start" : game.start, 
                    "end" : game.end, 
                    "blocked nodes": game.blocked_roads, 
                    "neighbours": game.get_neighbours_and_roads(game.current_pos), 
                    "optimal path" :  game.optimal_path, 
                    "optimal distance" : game.optimal_distance})

def send_neighbours(data: dict) -> dict:
    """
    calls generate neighbours and sends to the UI a JSON file with them
    :rtype dict:
    """
    return jsonify({"neighbours": game.get_neighbours_and_roads(data["current"])})


@app.route('/main', methods=['POST'])
def main() -> dict:
    """
    processes the inputs from the webpage
    :rtype dict:
    """
    data = request.get_json()
    
    if data["type"] == "start":
        return send_start(data)
    elif data["type"] == "neighbours":
        return send_neighbours(data)
 
    
    return jsonify({"error" : "The data is not a JSON or the format is invalid"}), 400


if __name__ == "__main__":
    # run the server, open it on all ports
    app.run(debug=True, host='0.0.0.0', port=5000)