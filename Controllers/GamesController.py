from flask import Blueprint, jsonify, request
from Services import GamesService


routes = Blueprint('GamesController', __name__)

#Get all Games
@routes.route('/api/games', methods=['GET'])
def get_all_games():
    try:
        games = GamesService.get_all_games()
        return jsonify(games)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Post new Game
@routes.route('/api/games', methods=['POST'])
def save_to_table_storage():
    try:
        data = request.json
        data = GamesService.save_to_table_storage(data)
        return 'succes', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#Get Game by video id and type
@routes.route('/api/games/<videoId>/<type>', methods=['GET'])
def find_game_by_video_id_and_type(videoId, type):
    #get video id
    try:
        game = GamesService.find_game_by_video_id_and_type(videoId, type)
        return jsonify(game)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Update GameId
@routes.route('/api/games/<gameId>', methods=['PUT'])
def update_game_id(gameId):
    #update game id
    newId = request.json()
    try:
        game = GamesService.update_game_id(gameId,gameId,newId)
        return jsonify(game)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Delete Game by Game ID
@routes.route('/api/games/<gameId>', methods=['DELETE'])
def delete_game_by_id(gameId):
    #delete Game
    try:
        game = GamesService.delete_game_by_id(gameId)
        return jsonify(game)
    except Exception as e:
        return jsonify({"error": str(e)}), 500