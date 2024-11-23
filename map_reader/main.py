from Map import Map
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


class SendData:
    def __init__(self, data):
        self.map = Map("complex_graph.json", data["difficulty"])

    def send_start(self):
        """
        sends the start, end and blocked nodes to the UI in a JSON file
        """
        
        return jsonify({"start" : self.map.start, 
                        "end" : self.map.end, 
                        "blocked nodes": self.map.blocked_roads, 
                        "neighbours": self.map.get_neighbours_and_roads(self.map.current_pos), 
                        "optimal path" :  self.map.optimal_path, 
                        "optimal distance" : self.map.optimal_distance})

    def send_neighbours(self, data):
        """
        calls generate neighbours and sends to the UI a JSON file with them
        """
        self.map.process_inputs(data["current"])
        return jsonify({self.map.get_neighbours_and_roads(self.map.current_pos)})


@app.route('/main', methods=['POST'])
def main():
    """
    processes the inputs from the webpage
    """
    data = request.get_json()
    
    print("Received data:", data)  # Debugging :)
    
    if data["type"] == "start":
        # initialize the map object and return the starting information for the frontend
        send_data = SendData(data)
        return send_data.send_start()
    elif data["type"] == "neighbours":
        return send_data.send_neighbours(data)
 
    
    return jsonify({"error" : "The data is not a JSON or the format is invalid"}), 400


if __name__ == "__main__":
    app.run(debug=True)

#testing if some functions work properly
#Graph = gr.GeoGraph("map_complex.geojson")
#print(Graph.G.nodes)
#Map = Map.Map(Graph)
#print(Map.generate_start_end(1000))