from flask import Blueprint, jsonify, request
from models import Game
from azure.storage.blob import BlobServiceClient
import os
import json

routes = Blueprint('routes', __name__)

# Azure Storage configuration
#AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
#BLOB_SERVICE_CLIENT = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

#dummy data
games = [
    {'id': 1, 'videoId': 100001},
    {'id': 2, 'videoId': 100002}
]
#gamenew = Game(3,100003)
#games.append(gamenew.__dict__)
memorygames = []
objectgames = []
findobjectgames = []
pointatpicturegames = []

#######################################################################
#GAMES

#Get all Games
@routes.route('/api/games', methods=['GET'])
def getGames():
    #Connect to Azure 
    #Get games
    #Return them into list based on Model
    try:
        return jsonify(games)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Post new Game
@routes.route('/api/games', methods=['POST'])
def addGame():
    try:
        # id = request.get_json['id']
        # videoId = request.get_json['videoId']
        # new_game = Game(id,videoId)
        # games.append(new_game.__dict__)
        games.append(request.get_json())
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#Get Game by video id and type
@routes.route('/api/games/<videoId>/<type>', methods=['GET'])
def getGameByVideoAndType(videoId, type):
    #get video id
    try:
        return jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Update GameId
@routes.route('/api/games/<gameId>', methods=['PUT'])
def updateGame(gameId):
    #update game id
    try:
        return jsonify(gameId)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Delete Game by Game ID
@routes.route('/api/games/<gameId>', methods=['DELETE'])
def deleteGame(gameId):
    #delete Game
    try:
        return jsonify(gameId)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#######################################################################
#MEMORY GAME

