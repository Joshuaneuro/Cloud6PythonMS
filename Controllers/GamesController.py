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
        def create_game():
            return self.create_game()

        @self.routes.route('/api/games/<string:video_id>/<string:game_type>', methods=['GET'])
        def find_game_by_video_id_and_type(video_id, game_type):
            return self.find_game_by_video_id_and_type(video_id, game_type)

        @self.routes.route('/api/games/<string:video_id>/<string:game_type>', methods=['PATCH'])
        def update_game(video_id, game_type):
            return self.update_game(video_id, game_type)

        @self.routes.route('/api/games/<string:partition_key>/<string:row_key>', methods=['PUT'])
        def update_game_id(partition_key, row_key):
            return self.update_game_id(partition_key, row_key)

        @self.routes.route('/api/games/<string:game_id>', methods=['DELETE'])
        def delete_game_by_id(game_id):
            return self.delete_game_by_id(game_id)

    def get_all_games(self):
        try:
            # Get query parameters
            page = request.args.get('page', default=1, type=int)
            page_size = request.args.get('pageSize', default=10, type=int)
            video_id = request.args.get('videoId', default=None, type=str)
            game_type = request.args.get('gameType', default=None, type=str)

            # Call service layer with the parameters
            games, total_count = self.service.get_all_games(page, page_size, video_id, game_type)

            # Return paginated response
            return jsonify({
                "games": games,
                "totalRecords": total_count,
                "page": page,
                "pageSize": page_size
            }), 200
        except Exception as e:
            logging.error(f"Error retrieving games: {str(e)}")
            return jsonify({"error": "Failed to retrieve games"}), 500

    def create_game(self):
        try:
            # Parse metadata from the form data
            metadata = json.loads(request.form.get('metadata', '{}'))
            if not metadata:
                return jsonify({"error": "Metadata is required"}), 400

            # Collect all files dynamically
            files = {key: request.files.get(key) for key in request.files.keys()}

            # Validate metadata and files
            if not files:
                return jsonify({"error": "At least one file is required"}), 400

            # Call the service to create the game
            self.service.create_game(metadata, files)

            return jsonify({"message": "Game created successfully"}), 201
        except ValueError as ve:
            logging.warning(f"Validation error: {str(ve)}")
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            logging.error(f"Error creating game: {str(e)}")
            return jsonify({"error": "Failed to create game"}), 500


    def find_game_by_video_id_and_type(self, video_id, game_type):
        try:
            if not video_id or not game_type:
                logging.warning("Invalid video_id or game_type")
                return jsonify({"error": "Invalid video_id or game_type"}), 400
            game = self.service.find_game_by_video_id_and_type(video_id, game_type)
            if not game:
                return jsonify({"error": "Game not found"}), 404
            return jsonify({"game": game}), 200
        except ValueError as ve:
            logging.warning(f"Validation error: {str(ve)}")
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            logging.error(f"Error finding game: {str(e)}")
            return jsonify({"error": "Failed to find game"}), 500

    def update_game(self, video_id, game_type):
        try:
            data = request.form.to_dict()
            file = request.files.get('file')  # Get the optional file from the request

            if not data and not file:
                return jsonify({"error": "No data or file provided for update"}), 400

            # Call the service to handle the update
            self.service.update_game(video_id, game_type, data, file)
            return jsonify({"message": "Game updated successfully"}), 200
        except ValueError as ve:
            logging.warning(f"Validation error: {str(ve)}")
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            logging.error(f"Error updating game: {str(e)}")
            return jsonify({"error": "Failed to update game"}), 500

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
            if not game_id:
                logging.warning("Missing game_id in request")
                return jsonify({"error": "Missing game_id in request"}), 400
            self.service.delete_game_by_id(game_id)
            return jsonify({"message": "Game deleted successfully"}), 200
        except ValueError as ve:
            logging.warning(f"Validation error: {str(ve)}")
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            logging.error(f"Error deleting game: {str(e)}")
            return jsonify({"error": "Failed to delete game"}), 500
