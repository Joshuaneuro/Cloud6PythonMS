from flask import Blueprint, jsonify, request
from models import Game
from azure.storage.blob import BlobServiceClient
import os

routes = Blueprint('routes', __name__)

# Azure Storage configuration
#AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
#BLOB_SERVICE_CLIENT = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

games = []
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
    return jsonify()

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

# @routes.route('/list-blobs', methods=['GET'])
# def list_blobs():
#     container_name = request.args.get('container')
    
#     if not container_name:
#         return jsonify({"error": "Container name is required"}), 400

#     try:
#         container_client = BLOB_SERVICE_CLIENT.get_container_client(container_name)
#         blobs = container_client.list_blobs()
#         blob_list = [{"name": blob.name, "size": blob.size} for blob in blobs]

#         return jsonify({"blobs": blob_list})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @routes.route('/upload-blob', methods=['POST'])
# def upload_blob():
#     container_name = request.form.get('container')
#     file = request.files.get('file')

#     if not container_name or not file:
#         return jsonify({"error": "Container name and file are required"}), 400

#     try:
#         container_client = BLOB_SERVICE_CLIENT.get_container_client(container_name)
#         blob_client = container_client.get_blob_client(file.filename)
#         blob_client.upload_blob(file, overwrite=True)

#         return jsonify({"message": f"File {file.filename} uploaded successfully to container {container_name}."})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

