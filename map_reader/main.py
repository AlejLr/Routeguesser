from Map import Map
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# initialize the map object globally so that it can be used dynamically by the server, 
# when frontend sends requests with updated player position
game = Map("complex_graph2.json")

def send_start(data):
    """
    sends the start, end and blocked nodes to the UI in a JSON file
    Keep tracks of the round to reset start and end when needed
    """
    game.game_init(data["difficulty"])
    return jsonify({"start" : game.start, 
                    "end" : game.end, 
                    "blocked nodes": game.blocked_roads, 
                    "neighbours": game.get_neighbours_and_roads(game.current_pos), 
                    "optimal path" :  game.optimal_path, 
                    "optimal distance" : float(game.optimal_distance)})

def send_neighbours(data):
    """
    calls generate neighbours and sends to the UI a JSON file with them
    """
    return jsonify({"neighbours": game.get_neighbours_and_roads(data["current"])})


@app.route('/main', methods=['POST'])
def main():
    """
    processes the inputs from the webpage
    """
    data = request.get_json()
    
    #print("Received data:", data)  # Debugging :)
    
    
    if data["type"] == "start":
        return send_start(data)
    elif data["type"] == "neighbours":
        return send_neighbours(data)
 
    
    return jsonify({"error" : "The data is not a JSON or the format is invalid"}), 400


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)