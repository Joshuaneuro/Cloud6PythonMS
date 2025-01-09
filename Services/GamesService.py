from DAL import GameReposity
from Domain.FindAllObjectsGame import FindAllObjectsGame
from Domain.MemoryGame import MemoryGame
from Domain.PointAtPictureGame import PointAtPictureGame
from Domain.ObjectPlacement import ObjectPlacement
from typing import Union
import json

#SET UP TABLE STORAGE
GameReposity.table_set_up()

## OBJECT FUNCTIONS

# CREATE GAME OBJECT FROM JSON
def create_game_from_json(json_data) -> Union[MemoryGame, FindAllObjectsGame, PointAtPictureGame]:
    data = json.loads(json_data)
    print(data)
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

## CREATE GAME OBJECT FROM TABLESTORAGE JSON
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


## FUNCTIONS LOGIC
def get_all_games():

    data = GameReposity.get_all_games()
    
    return data

def save_to_table_storage(data):
    
    print(data)
    x = create_game_from_json(json.dumps(data))
    print("________________________________________")
    print(x)
    x = transform_to_entity(x)
    data = GameReposity.save_to_table_storage(x)

    return data

def delete_game_by_id(game_id: int):

    data = GameReposity.delete_game_by_id(game_id)

    return data

def find_game_by_video_id_and_type(video_id: str, game_type: str):

    data = GameReposity.find_game_by_video_id_and_type(video_id,game_type)

    return data

def update_game_id(gameId,newId):

    data = GameReposity.update_game_id(gameId,newId)

    return data