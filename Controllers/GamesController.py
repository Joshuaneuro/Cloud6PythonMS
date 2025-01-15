from flask import Blueprint, jsonify, request
from Services.GamesService import GamesService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class GamesController:
    def __init__(self, service=None):
        self.service = service or GamesService()
        self.routes = Blueprint('games_controller', __name__)
        self._register_routes()

    def _register_routes(self):
        @self.routes.route('/api/games', methods=['GET'])
        def get_all_games():
            return self.get_all_games()

        @self.routes.route('/api/games', methods=['POST'])
        def save_to_table_storage():
            return self.save_to_table_storage()

        @self.routes.route('/api/games/<string:video_id>/<string:game_type>', methods=['GET'])
        def find_game_by_video_id_and_type(video_id, game_type):
            return self.find_game_by_video_id_and_type(video_id, game_type)

        @self.routes.route('/api/games/<string:partition_key>/<string:row_key>', methods=['PUT'])
        def update_game_id(partition_key, row_key):
            return self.update_game_id(partition_key, row_key)

        @self.routes.route('/api/games/<string:game_id>', methods=['DELETE'])
        def delete_game_by_id(game_id):
            return self.delete_game_by_id(game_id)

    def get_all_games(self):
        try:
            games = self.service.get_all_games()
            return jsonify({"games": games}), 200
        except Exception as e:
            logging.error(f"Error retrieving games: {str(e)}")
            return jsonify({"error": "Failed to retrieve games"}), 500

    def save_to_table_storage(self):
        try:
            data = request.json
            if not data:
                return jsonify({"error": "Invalid request data"}), 400
            self.service.save_to_table_storage(data)
            return jsonify({"message": "Game saved successfully"}), 201
        except ValueError as ve:
            logging.warning(f"Validation error: {str(ve)}")
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            logging.error(f"Error saving game: {str(e)}")
            return jsonify({"error": "Failed to save game"}), 500

    def find_game_by_video_id_and_type(self, video_id, game_type):
        try:
            game = self.service.find_game_by_video_id_and_type(video_id, game_type)
            if not game:
                return jsonify({"error": "Game not found"}), 404
            return jsonify({"game": game}), 200
        except Exception as e:
            logging.error(f"Error finding game: {str(e)}")
            return jsonify({"error": "Failed to find game"}), 500

    def update_game_id(self, partition_key, row_key):
        try:
            data = request.json
            new_id = data.get("new_id")
            if not new_id:
                return jsonify({"error": "Missing new_id in request"}), 400
            self.service.update_game_id(partition_key, row_key, new_id)
            return jsonify({"message": "Game ID updated successfully"}), 200
        except ValueError as ve:
            logging.warning(f"Validation error: {str(ve)}")
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            logging.error(f"Error updating game ID: {str(e)}")
            return jsonify({"error": "Failed to update game ID"}), 500

    def delete_game_by_id(self, game_id):
        try:
            self.service.delete_game_by_id(game_id)
            return jsonify({"message": "Game deleted successfully"}), 200
        except Exception as e:
            logging.error(f"Error deleting game: {str(e)}")
            return jsonify({"error": "Failed to delete game"}), 500
