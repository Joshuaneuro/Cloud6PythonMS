from flask import Blueprint, jsonify, request
from Services import GameService

routes = Blueprint('GamesController', __name__)
service = GameService()

@routes.route('/api/games', methods=['GET'])
def get_all_games():
    try:
        games = service.get_all_games()
        return jsonify(games)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/api/games', methods=['POST'])
def save_to_table_storage():
    try:
        data = request.json
        service.save_to_table_storage(data)
        return 'success', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/api/games/<videoId>/<type>', methods=['GET'])
def find_game_by_video_id_and_type(videoId, type):
    try:
        game = service.find_game_by_video_id_and_type(videoId, type)
        return jsonify(game)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/api/games/<partitionKey>/<rowKey>', methods=['PUT'])
def update_game_id(partitionKey, rowKey):
    try:
        new_id = request.json.get("newId")
        service.update_game_id(partitionKey, rowKey, new_id)
        return 'success', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/api/games/<gameId>', methods=['DELETE'])
def delete_game_by_id(gameId):
    try:
        service.delete_game_by_id(gameId)
        return 'success', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500
