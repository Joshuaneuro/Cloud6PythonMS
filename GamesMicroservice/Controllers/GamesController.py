from flask import Blueprint, jsonify, request
import json


routes = Blueprint('routes', __name__)

#Get all Games
@routes.route('/api/games', methods=['GET'])
def getGames():
    try:
        games = get_all_games(connectionstring, TABLE_NAME)
        return jsonify(games)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Post new Game
@routes.route('/api/games', methods=['POST'])
def addGame():
    try:
        data = request.json
        new_game = create_game_from_json(json.dumps(data))
        save_to_table_storage(connectionstring, TABLE_NAME,new_game)
        return 'Succes', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#Get Game by video id and type
@routes.route('/api/games/<videoId>/<type>', methods=['GET'])
def getGameByVideoAndType(videoId, type):
    #get video id
    try:
        game = find_game_by_video_id_and_type(connectionstring, TABLE_NAME,videoId, type)
        return jsonify(game)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Update GameId
@routes.route('/api/games/<gameId>', methods=['PUT'])
def updateGame(gameId):
    #update game id
    newId = request.json()
    game = update_game_id(connectionstring,TABLE_NAME,gameId,gameId,newId)
    try:
        return jsonify(game)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Delete Game by Game ID
@routes.route('/api/games/<gameId>', methods=['DELETE'])
def deleteGame(gameId):
    #delete Game
    try:
        game = delete_game_by_id(connectionstring,TABLE_NAME,gameId)
        return jsonify(game)
    except Exception as e:
        return jsonify({"error": str(e)}), 500