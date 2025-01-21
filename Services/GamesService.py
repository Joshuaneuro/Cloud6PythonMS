import json
from typing import Union
from DAL.GameRepository import GameRepository
from Domain.FindAllObjectsGame import FindAllObjectsGame
from Domain.MemoryGame import MemoryGame
from Domain.PointAtPictureGame import PointAtPictureGame
from Domain.ObjectPlacement import ObjectPlacement
import logging

class GamesService:
    def __init__(self, repository: GameRepository = None):
        self.repository = repository if repository else GameRepository()

    def get_all_games(self, page: int, page_size: int, video_id: str = None, game_type: str = None) -> Tuple[List[dict], int]:
        """
        Retrieves all games with optional filters and pagination.
        
        """
        try:
            offset = (page - 1) * page_size
            games, total_count = self.repository.get_all_games(offset, page_size, video_id, game_type)
            return games, total_count
        except Exception as e:
            logging.error(f"Error retrieving games: {str(e)}")
            raise
    
    def find_game_by_video_id_and_type(self, video_id: str, game_type: str):
        try:
            if not video_id or not isinstance(video_id, str):
                raise ValueError("Invalid video_id provided.")
            if not game_type or not isinstance(game_type, str):
                raise ValueError("Invalid game_type provided.")
            return self.repository.find_game_by_video_id_and_type(video_id, game_type)
        except Exception as e:
            logging.error(f"Error finding game by video_id and type: {str(e)}")
            raise

    def create_game(self, metadata: dict, files: dict) -> None:
        try:
            # Validate game type
            game_type = metadata.get("type")
            if not game_type:
                raise ValueError("Game type is required in metadata.")

            # Upload files to blob storage and update metadata
            for key, file in files.items():
                blob_name = f"{metadata['id']}/{key}_{file.filename}"  # Generate blob name
                blob_url = self.repository.upload_to_blob(file, blob_name)  # Upload file
                # Update metadata with both blob URL and blob name
                self.update_metadata_with_blob_info(metadata, key, blob_url, blob_name)

            # Create game entity and save to table storage
            game = self.create_game_from_json(json.dumps(metadata))
            entity = self.transform_to_entity(game)
            self.repository.save_to_table_storage(entity)

            logging.info(f"Game of type '{game_type}' created successfully with ID {game.id}.")
        except Exception as e:
            logging.error(f"Error creating game: {str(e)}")
            raise

    def update_metadata_with_blob_info(self, metadata: dict, key: str, blob_url: str, blob_name: str):
        """
        Updates the metadata to include both blob URL and blob name directly.
        If there are multiple files, it appends to the list.
        """
        if isinstance(metadata.get(key), list):  # Handle lists of files
            # Append new URLs and names to the existing lists
            metadata[key]["blobUrls"].append(blob_url)
            metadata[key]["blobNames"].append(blob_name)
        else:  # Handle single file
            metadata[key] = {"blobUrl": blob_url, "blobName": blob_name}

    def update_game(self, video_id: str, game_type: str, updated_data: dict, file=None):
        try:
            # Fetch the existing entity
            existing_entity = self.repository.find_game_by_video_id_and_type(video_id, game_type)
            if not existing_entity:
                raise ValueError(f"Game with videoId {video_id} and gameType {game_type} not found.")

            # Handle file upload if a new file is provided
            if file:
                # Construct a unique blob name (e.g., "videoId/gameType/filename")
                blob_name = f"{video_id}/{game_type}/{file.filename}"
                new_blob_url = self.repository.upload_to_blob(file, blob_name)

                # Update the corresponding media field in the entity
                if "imageUrls" in updated_data:
                    updated_data["imageUrls"] = new_blob_url
                elif "backgroundImageUrl" in updated_data:
                    updated_data["backgroundImageUrl"] = new_blob_url
                elif "soundUrl" in updated_data:
                    updated_data["soundUrl"] = new_blob_url
                # Add more cases as needed for different game types

            # Update the fields in the entity with the new data
            for key, value in updated_data.items():
                existing_entity[key] = value

            # Save the updated entity
            self.repository.save_to_table_storage(existing_entity)
            logging.info(f"Game with videoId {video_id} and gameType {game_type} updated successfully.")
        except Exception as e:
            logging.error(f"Error updating game: {str(e)}")
            raise

    def delete_game_by_id(self, game_id: int):
        try:
            if not isinstance(game_id, int):
                raise ValueError("Invalid game_id provided.")
            self.repository.delete_game_by_id(game_id)
            logging.info(f"Game with ID {game_id} deleted successfully.")
        except ValueError as ve:
            logging.warning(f"Validation failed: {str(ve)}")
            raise
        except Exception as e:
            logging.error(f"Error deleting game: {str(e)}")
            raise

    def update_game_id(self, partition_key: str, row_key: str, new_game_id: int):
        try:
            self.repository.update_game_id(partition_key, row_key, new_game_id)
            logging.info(f"Updated game_id to {new_game_id} for PartitionKey {partition_key} and RowKey {row_key}.")
        except Exception as e:
            logging.error(f"Error updating game ID: {str(e)}")
            raise

    def create_game_from_json(self, json_data) -> Union[MemoryGame, FindAllObjectsGame, PointAtPictureGame]:
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")

        # Extracting core metadata fields
        core_fields = ["id", "type", "videoId", "blobUrl", "blobName"]
        metadata = {key: value for key, value in data.items() if key not in core_fields}

        # Determine game type and create corresponding game object
        game_type = data.get("type")
        if game_type == "MemoryGame":
            return MemoryGame(
                data["id"],
                data["videoId"],
                [file["blobUrl"] for file in metadata["imageFiles"]],  # Now imageFiles are URLs
            )
        elif game_type == "FindAllObjectsGame":
            objects = [
                ObjectPlacement(
                    obj["blobUrls"][0],  # Use blobUrl for each object
                    obj["x"], 
                    obj["y"]
                ) 
                for obj in metadata["objects"]
            ]
            return FindAllObjectsGame(
                data["id"], 
                data["videoId"], 
                metadata["backgroundFile"]["blobUrl"],  # Use blobUrl for backgroundFile
                objects
            )
        elif game_type == "PointAtPictureGame":
            return PointAtPictureGame(
                data["id"], 
                data["videoId"],
                metadata["correctFile"]["blobUrl"],  # Use blobUrl for correctFile
                [file["blobUrl"] for file in metadata["incorrectFiles"]],  # Use blobUrl for incorrectFiles
                metadata["soundFile"]["blobUrl"]  # Use blobUrl for soundFile
            )
        else:
            raise ValueError(f"Unknown game type: {game_type}")


    def transform_to_entity(self, game) -> dict:
        base_entity = {
            "PartitionKey": str(game.id),
            "RowKey": type(game).__name__,
            "videoId": game.videoId,
            "blobUrl": game.blob_url,
            "blobName": game.blob_name,  # Ensure blobName is added here
        }

        # Add metadata fields if available
        if hasattr(game, "metadata") and game.metadata:
            base_entity.update(game.metadata)

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
