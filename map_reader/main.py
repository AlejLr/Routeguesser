from Map import Map
from flask import Flask, request, jsonify, wrappers
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


def send_start(data: dict) -> wrappers.Response:
    """
    Sends the start, end and blocked nodes to the UI in a JSON file
    Keep tracks of the round to reset start and end when needed

    :return (JSON): The starting data required to initiate the game.
    """
    game.game_init(data["difficulty"])
    return jsonify({"start": game.start, 
                    "end": game.end, 
                    "blocked nodes": game.blocked_roads, 
                    "neighbours": game.get_neighbours_and_roads(game.start),
                    "optimal path": game.optimal_path, 
                    "optimal distance": game.optimal_distance})

def send_neighbours(data: dict[str]) -> wrappers.Response:
    """
    Calls generate neighbours and sends to the UI a JSON file with them.

    :param data (dict): The current game data.

    :return (JSON): The neighbours of the current node.
    """
    return jsonify({"neighbours": game.get_neighbours_and_roads(data["current"])})


@app.route('/main', methods=['POST'])
def main() -> tuple[wrappers.Response, int]:
    """
    Processes the inputs from the webpage.

    :return (JSON): The results of the input processing.
    """
    data = request.get_json()
    
    if data["type"] == "start":
        return send_start(data), 0
    elif data["type"] == "neighbours":
        return send_neighbours(data), 0
 
    
    return jsonify({"error" : "The data is not a JSON or the format is invalid"}), 400


if __name__ == "__main__":
    # run the server, open it on all ports
    app.run(debug=True, host='0.0.0.0', port=5000)