import json
from typing import Union
from DAL.GameRepository import GameRepository
from Domain.FindAllObjectsGame import FindAllObjectsGame
from Domain.MemoryGame import MemoryGame
from Domain.PointAtPictureGame import PointAtPictureGame
from Domain.ObjectPlacement import ObjectPlacement

class GamesService:
    def __init__(self):
        self.repository = GameRepository()

    def create_game_from_json(self, json_data) -> Union[MemoryGame, FindAllObjectsGame, PointAtPictureGame]:
        data = json.loads(json_data)
        game_type = data.get("type")
        if game_type == "MemoryGame":
            return MemoryGame(data["id"], data["videoId"], data["imageUrls"])
        elif game_type == "FindAllObjects":
            objects = [ObjectPlacement(**obj) for obj in data["objects"]]
            return FindAllObjectsGame(data["id"], data["videoId"], data["backgroundImageUrl"], objects)
        elif game_type == "PointAtPictureGame":
            return PointAtPictureGame(data["id"], data["videoId"], data["correctImageUrl"], data["incorrectImagesUrls"], data["soundUrl"])
        else:
            raise ValueError(f"Unknown game type: {game_type}")

    def transform_to_entity(self, game) -> dict:
        base_entity = {
            "PartitionKey": str(game.id),
            "RowKey": type(game).__name__,
            "videoId": game.videoId,
        }
        if isinstance(game, MemoryGame):
            base_entity["imageUrls"] = ",".join(game.imageUrls)
        elif isinstance(game, FindAllObjectsGame):
            base_entity["backgroundImageUrl"] = game.backgroundImageUrl
            base_entity["objects"] = ",".join([f"{obj.objectImageUrl}:{obj.x}:{obj.y}" for obj in game.objects])
        elif isinstance(game, PointAtPictureGame):
            base_entity.update({
                "correctImageUrl": game.correctImageUrl,
                "incorrectImagesUrls": ",".join(game.incorrectImageUrls),
                "soundUrl": game.soundUrl,
            })
        return base_entity

    def save_to_table_storage(self, data):
        game = self.create_game_from_json(json.dumps(data))
        entity = self.transform_to_entity(game)
        self.repository.save_to_table_storage(entity)

    def get_all_games(self):
        return self.repository.get_all_games()

    def delete_game_by_id(self, game_id: int):
        self.repository.delete_game_by_id(game_id)

    def find_game_by_video_id_and_type(self, video_id: str, game_type: str):
        return self.repository.find_game_by_video_id_and_type(video_id, game_type)

    def update_game_id(self, partition_key: str, row_key: str, new_game_id: int):
        self.repository.update_game_id(partition_key, row_key, new_game_id)
