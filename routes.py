from flask import Blueprint, jsonify, request
from models import Game
from azure.storage.blob import BlobServiceClient
import os

routes = Blueprint('routes', __name__)

# Azure Storage configuration
#AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
#BLOB_SERVICE_CLIENT = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

games = []
memorygames = []
objectgames = []
findobjectgames = []
pointatpicturegames = []

#Get all Games
@routes.route('/api/games', methods=['GET'])
def getGames():
    #Connect to Azure 
    #Get games
    #Return them into list based on Model
    return jsonify(games)

#Post new Game
@routes.route('/api/games', methods=['POST'])
def addGame():
    id = request.json('id')
    videoId = request.json('videoId')
    new_game = Game(id,videoId)
    games.append(new_game.__dict__)
    return jsonify(new_game.__dict__)

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
    return jsonify()

#Delete Game by Game ID
@routes.route('/api/games/<gameId>', methods=['DELETE'])
def deleteGame(gameId):
    #delete Game
    return jsonify()