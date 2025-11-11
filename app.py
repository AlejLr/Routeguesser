import os
from flask import Flask, request, jsonify, send_from_directory
from map_reader.Map import Map

def create_app():
    app = Flask(__name__, static_folder="FrontEnd", static_url_path="")

    @app.get("/")
    def root():
        return send_from_directory(app.static_folder, "game.html")

    @app.get("/game.html")
    def game():
        return send_from_directory(app.static_folder, "game.html")

    @app.get("/<path:path>")
    def static_files(path):
        return send_from_directory(app.static_folder, path)

    game = Map(os.path.join("map_reader", "map_graph.json"))

    def send_start(data: dict):
        game.game_init(data["difficulty"])
        return jsonify({
            "start": game.start,
            "end": game.end,
            "blocked nodes": game.blocked_roads,
            "neighbours": game.get_neighbours_and_roads(game.start),
            "optimal path": game.optimal_path,
            "optimal distance": game.optimal_distance
        })
    
    def send_neighbours(data: dict):
        return jsonify({"neighbours": game.get_neighbours_and_roads(data["current"])})
    
    @app.post("/api/main")
    def api_main():
        data = request.get_json(silent=True) or {}
        t = data.get("type")
        if t == "start":
            return send_start(data)
        elif t == "neighbours":
            return send_neighbours(data)
        return jsonify({"error":"invalid payload"}), 400

    @app.get("/healthz")
    def health():
        return "ok", 200
    
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
