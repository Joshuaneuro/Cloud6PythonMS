from azure.data.tables import TableServiceClient
from azure.core.exceptions import ResourceExistsError
from dotenv import load_dotenv
import os

class GameRepository:
    def __init__(self):
        load_dotenv()
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.table_name = "GamesTable"
        self.table_service = TableServiceClient.from_connection_string(conn_str=self.connection_string)
        self._table_set_up()

    def _table_set_up(self):
        try:
            self.table_service.create_table(self.table_name)
            print(f"Table '{self.table_name}' created.")
        except ResourceExistsError:
            print(f"Table '{self.table_name}' already exists.")
    
    def get_all_games(self):
        table_client = self.table_service.get_table_client(self.table_name)
        return list(table_client.list_entities())

    def save_to_table_storage(self, data):
        table_client = self.table_service.get_table_client(self.table_name)
        table_client.upsert_entity(data)
        print(f"Saved {data['PartitionKey']} with RowKey {data['RowKey']} to table {self.table_name}")

    def delete_game_by_id(self, game_id: int):
        table_client = self.table_service.get_table_client(self.table_name)
        filter_query = f"PartitionKey eq {game_id}"
        entities = table_client.query_entities(filter_query)
        for entity in entities:
            table_client.delete_entity(partition_key=entity["PartitionKey"], row_key=entity["RowKey"])
            print(f"Deleted game with id={game_id} from table {self.table_name}.")
            return
        print(f"No game found with id={game_id} in table {self.table_name}.")

    def find_game_by_video_id_and_type(self, video_id: str, game_type: str):
        table_client = self.table_service.get_table_client(self.table_name)
        query_filter = f"PartitionKey eq '{video_id}' and RowKey eq '{game_type}'"
        entities = table_client.query_entities(query_filter)
        for entity in entities:
            return entity
        return None

    def update_game_id(self, partition_key: str, row_key: str, new_game_id: int):
        table_client = self.table_service.get_table_client(self.table_name)
        entity = table_client.get_entity(partition_key=partition_key, row_key=row_key)
        entity["game_id"] = new_game_id
        table_client.upsert_entity(entity)
        print(f"Updated game_id to {new_game_id} for {partition_key} with RowKey {row_key}")
