from flask import Blueprint, jsonify, request
from models import MemoryGame, FindAllObjectsGame, PointAtPictureGame,ObjectPlacement
from dotenv import load_dotenv
import os
import json
import logging
from typing import Union
from azure.data.tables import TableServiceClient
from azure.core.exceptions import ResourceExistsError


routes = Blueprint('routes', __name__)

#this needs to be changed locally but this is global local azurite connection string
load_dotenv()
connectionstring = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
TABLE_NAME = "GamesTable"
table_service_client = TableServiceClient.from_connection_string(conn_str=connectionstring)

#Ensure the table exists
try:
    table_client = table_service_client.create_table(TABLE_NAME)
    print(f"Table '{TABLE_NAME}' created.")
except ResourceExistsError:
    table_client = table_service_client.get_table_client(TABLE_NAME)
    print(f"Table '{TABLE_NAME}' already exists.")


def create_game_from_json(json_data) -> Union[MemoryGame, FindAllObjectsGame, PointAtPictureGame]:
    data = json.loads(json_data)
    type = data.get("type")
    id = data.get("id")
    videoId = data.get("videoId")

    if type == "MemoryGame":
        return MemoryGame(id, videoId, data["imageUrls"])
    elif type == "FindAllObjects":
        objects = [ObjectPlacement(**obj) for obj in data["objects"]]
        return FindAllObjectsGame(id, videoId, data["backgroundImageUrl"], objects)
    elif type == "PointAtPictureGame":
        return PointAtPictureGame(
            id,
            videoId,
            data["correctImageUrl"],
            data["incorrectImagesUrls"],
            data["soundUrl"]
        )
    else:
        raise ValueError(f"Unknown game type: {type}")

def create_game_from_json_output(json_data) -> Union[MemoryGame, FindAllObjectsGame, PointAtPictureGame]:
    data = json.loads(json_data)
    type = data.get("RowKey")
    id = data.get("PartitionKey")
    videoId = data.get("videoId")

    if type == "MemoryGame":
        return MemoryGame(id, videoId, data["imageUrls"])
    elif type == "FindAllObjects":
        objects = [ObjectPlacement(**obj) for obj in data["objects"]]
        return FindAllObjectsGame(id, videoId, data["backgroundImageUrl"], objects)
    elif type == "PointAtPictureGame":
        return PointAtPictureGame(
            id,
            videoId,
            data["correctImageUrl"],
            data["incorrectImagesUrls"],
            data["soundUrl"]
        )
    else:
        raise ValueError(f"Unknown game type: {type}")



# Function to transform game objects into entities for Table Storage
def transform_to_entity(game) -> dict:
    base_entity = {
        "PartitionKey": str(game.id),  # Use class name as PartitionKey
        "RowKey": type(game).__name__,         # Use game_id as RowKey
        "videoId": game.videoId,
    }

    if isinstance(game, MemoryGame):
        base_entity.update({
            "imageUrls": ",".join(game.imageUrls)  # Convert list to a single string
        })
    elif isinstance(game, FindAllObjectsGame):
        base_entity.update({
            "backgroundImageUrl": game.backgroundImageUrl,
            "objects": ",".join(
                [f"{obj.objectImageUrl}:{obj.x}:{obj.y}" for obj in game.objects]
            )  # Serialize objects as strings
        })
    elif isinstance(game, PointAtPictureGame):
        base_entity.update({
            "correctImageUrl": game.correctImageUrl,
            "incorrectImagesUrls": ",".join(game.incorrectImageUrls),
            "soundUrl": game.soundUrl
        })
    else:
        raise ValueError(f"Unknown game type: {type(game).__name__}")

    return base_entity

# Function to save data to Azure Table Storage
def save_to_table_storage(connectionstring: str, table_name: str, game):
    # Create a table service client
    table_service = TableServiceClient.from_connection_string(conn_str=connectionstring)
    
    # Get the table client
    table_client = table_service.get_table_client(table_name)
    
    # Transform the game object into an entity
    entity = transform_to_entity(game)
    logging.warning(entity)
    # Insert or update the entity in the table
    table_client.upsert_entity(entity)
    print(f"Saved {entity['PartitionKey']} with RowKey {entity['RowKey']} to table {table_name}")

def delete_game_by_id(connection_string: str, table_name: str, game_id: int):

    # Create the table service client
    table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
    table_client = table_service.get_table_client(table_name)

    # Query for the entity with the specified game_id
    filter_query = f"PartitionKey eq {game_id}"
    entities = table_client.query_entities(filter_query)

    # Iterate through entities to find the first match
    for entity in entities:
        partition_key = entity["PartitionKey"]
        row_key = entity["RowKey"]
        
        # Delete the entity
        table_client.delete_entity(partition_key=partition_key, row_key=row_key)
        print(f"Deleted game with id={game_id} from table {table_name}.")
        return  # Exit after deleting the first match

    print(f"No game found with id={game_id} in table {table_name}.")

#get all the games
def get_all_games(connection_string: str, table_name: str):
    table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
    table_client = table_service.get_table_client(table_name)

    # Query all entities in the table
    entities = table_client.list_entities()

    # Return a list of all entities
    return list(entities)

def update_game_id(connection_string: str, table_name: str, partition_key: str, row_key: str, new_game_id: int):
    table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
    table_client = table_service.get_table_client(table_name)

    # Retrieve the entity
    entity = table_client.get_entity(partition_key=partition_key, row_key=row_key)
    
    # Update the `game_id` field
    entity["game_id"] = new_game_id
    
    # Upsert (update or insert) the entity back to the table
    table_client.upsert_entity(entity)
    print(f"Updated game_id to {new_game_id} for {partition_key} with RowKey {row_key}")

def find_game_by_video_id_and_type(connection_string: str, table_name: str, video_id: str, game_type: str):
    table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
    table_client = table_service.get_table_client(table_name)

    # Query for a single game by PartitionKey (video_id) and game type

    # Query for the specific entity
    query_filter = f"PartitionKey eq '{video_id}' and RowKey eq '{game_type}'"
    entities = table_client.query_entities(query_filter)

    print("entity")
    for entity in entities:
        print(entity)
        return entity
    
    return None  # If no match found

#######################################################################
#GAMES

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