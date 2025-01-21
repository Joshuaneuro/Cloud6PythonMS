from azure.data.tables import TableServiceClient
from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.core.exceptions import ResourceExistsError, AzureError
from dotenv import load_dotenv
import os
import logging

class GameRepository:
    def __init__(self):
        # load_dotenv()  # Commented out since it’s not required in a container environment
        self.table_connection_string = os.getenv("AZURE_TABLE_CONNECTION_STRING")
        self.blob_connection_string = os.getenv("AZURE_BLOB_CONNECTION_STRING")
        self.blob_container_name = "gamesmedia"

        logging.info(f"Connection strings loaded.")

        # Table setup
        if not self.table_connection_string:
            raise ValueError("Environment variable 'AZURE_TABLE_CONNECTION_STRING' is not set or is empty.")
        self.table_service = TableServiceClient.from_connection_string(conn_str=self.table_connection_string)
        self.table_name = "GamesTable"
        self._table_set_up()

        # Blob setup
        if not self.blob_connection_string:
            raise ValueError("Environment variable 'AZURE_BLOB_CONNECTION_STRING' is not set or is empty.")
        self.blob_service = BlobServiceClient.from_connection_string(conn_str=self.blob_connection_string)
        self._blob_set_up()

    def _table_set_up(self):
        try:
            self.table_service.create_table(self.table_name)
            logging.info(f"Table '{self.table_name}' created.")
        except ResourceExistsError:
            logging.info(f"Table '{self.table_name}' already exists.")

    def _blob_set_up(self):
        try:
            container_client = self.blob_service.get_container_client(self.blob_container_name)
            if not container_client.exists():
                container_client.create_container()
                logging.info(f"Blob container '{self.blob_container_name}' created.")
            else:
                logging.info(f"Blob container '{self.blob_container_name}' already exists.")
        except AzureError as e:
            logging.error(f"Failed to set up blob container: {str(e)}")
            raise

    def upload_to_blob(self, file, blob_name):
        try:
            container_client = self.blob_service.get_container_client(self.blob_container_name)
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.upload_blob(
                file,
                content_settings=ContentSettings(content_type=file.mimetype),
                overwrite=True
            )
            logging.info(f"File '{blob_name}' uploaded to blob storage.")
            return blob_client.url
        except AzureError as e:
            logging.error(f"Failed to upload file to blob storage: {str(e)}")
            raise
    
    def save_to_table_storage(self, data):
        try:
            table_client = self.table_service.get_table_client(self.table_name)
            table_client.upsert_entity(data)
            logging.info(f"Saved {data['PartitionKey']} with RowKey {data['RowKey']} to table {self.table_name}")
        except AzureError as e:
            logging.error(f"Failed to save entity to table storage: {str(e)}")
            raise
    
    def get_all_games(self, offset: int, page_size: int, video_id: str = None, game_type: str = None):
        table_client = self.table_service.get_table_client(self.table_name)
        query_filter = []

        # Add filtering conditions
        if video_id:
            query_filter.append(f"PartitionKey eq '{video_id}'")
        if game_type:
            query_filter.append(f"RowKey eq '{game_type}'")
        combined_filter = " and ".join(query_filter) if query_filter else None

        try:
            # Retrieve filtered entities
            logging.info(f"Querying games with filter: {combined_filter} and pagination offset={offset}, page_size={page_size}")
            entities = table_client.query_entities(query_filter=combined_filter)

            # Apply pagination
            entities_list = list(entities)
            paginated_entities = entities_list[offset:offset + page_size]
            logging.info(f"Successfully retrieved {len(paginated_entities)} games out of {len(entities_list)} total records.")
            return paginated_entities, len(entities_list)
        except AzureError as e:
            logging.error(f"Azure error while retrieving games with filter: {combined_filter}. Error: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while retrieving games with filter: {combined_filter}. Error: {str(e)}")
            raise
        finally:
            table_client.close()

    def delete_game_by_id(self, game_id: int):
        table_client = self.table_service.get_table_client(self.table_name)
        try:
            filter_query = f"PartitionKey eq '{game_id}'"
            entities = list(table_client.query_entities(filter_query))
            if not entities:
                logging.warning(f"No game found with id={game_id}.")
                return
            for entity in entities:
                table_client.delete_entity(partition_key=entity["PartitionKey"], row_key=entity["RowKey"])
                logging.info(f"Deleted game with id={game_id}.")
        except AzureError as e:
            logging.error(f"Failed to delete game with id={game_id}: {str(e)}")
            raise

    def delete_blob(self, blob_name):
        try:
            container_client = self.blob_service.get_container_client(self.blob_container_name)
            blob_client = container_client.get_blob_client(blob_name)
            if blob_client.exists():
                blob_client.delete_blob()
                logging.info(f"Deleted blob: {blob_name}")
        except AzureError as e:
            logging.error(f"Failed to delete blob: {str(e)}")
            raise

    def find_game_by_video_id_and_type(self, video_id: str, game_type: str):
        table_client = self.table_service.get_table_client(self.table_name)
        try:
            query_filter = f"PartitionKey eq '{video_id}' and RowKey eq '{game_type}'"
            entities = table_client.query_entities(query_filter)
            for entity in entities:
                return entity
            return None
        except AzureError as e:
            logging.error(f"Azure query error: {str(e)}")
            raise

    def update_game_id(self, partition_key: str, row_key: str, new_game_id: int):
        table_client = self.table_service.get_table_client(self.table_name)
        try:
            entity = table_client.get_entity(partition_key=partition_key, row_key=row_key)
            entity["game_id"] = new_game_id
            table_client.upsert_entity(entity)
            logging.info(f"Updated game_id to {new_game_id} for PartitionKey {partition_key} with RowKey {row_key}")
        except AzureError as e:
            logging.error(f"Failed to update game_id: {str(e)}")
            raise
