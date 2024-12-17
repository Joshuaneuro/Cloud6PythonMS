from flask import Blueprint, jsonify, request
from models import Game
from azure.storage.blob import BlobServiceClient
import os
import json
from azure.data.tables import TableServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError


routes = Blueprint('routes', __name__)

# Azure Storage configuration
#AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"
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

TABLE_NAME = "TestTable"

connectionstring = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"

#table_service_client = TableServiceClient(endpoint=AZURE_TABLE_ENDPOINT, credential=credential)

table_service_client = TableServiceClient.from_connection_string(connectionstring)

# Ensure the table exists
try:
    table_client = table_service_client.create_table(TABLE_NAME)
    print(f"Table '{TABLE_NAME}' created.")
except ResourceExistsError:
    table_client = table_service_client.get_table_client(TABLE_NAME)
    print(f"Table '{TABLE_NAME}' already exists.")

@routes.route("/add", methods=["POST"])
def add_entity():
    data = request.json
    partition_key = data.get("PartitionKey")
    row_key = data.get("RowKey")
    properties = {k: v for k, v in data.items() if k not in ["PartitionKey", "RowKey"]}

    if not partition_key or not row_key:
        return jsonify({"error": "PartitionKey and RowKey are required"}), 400

    entity = {"PartitionKey": partition_key, "RowKey": row_key, **properties}

    try:
        table_client.create_entity(entity=entity)
        return jsonify({"message": "Entity added successfully", "entity": entity}), 201
    except ResourceExistsError:
        return jsonify({"error": "Entity already exists"}), 409


@routes.route("/get/<partition_key>/<row_key>", methods=["GET"])
def get_entity(partition_key, row_key):
    try:
        entity = table_client.get_entity(partition_key=partition_key, row_key=row_key)
        return jsonify(entity)
    except ResourceNotFoundError:
        return jsonify({"error": "Entity not found"}), 404


@routes.route("/delete/<partition_key>/<row_key>", methods=["DELETE"])
def delete_entity(partition_key, row_key):
    try:
        table_client.delete_entity(partition_key=partition_key, row_key=row_key)
        return jsonify({"message": "Entity deleted successfully"})
    except ResourceNotFoundError:
        return jsonify({"error": "Entity not found"}), 404


@routes.route("/list", methods=["GET"])
def list_entities():
    entities = table_client.list_entities()
    return jsonify([entity for entity in entities])