from azure.data.tables import TableServiceClient
from azure.core.exceptions import ResourceExistsError
from dotenv import load_dotenv
import os

#load .env
load_dotenv()

# Get Variables from .env
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
TABLE_NAME = "GamesTable"

table_service = TableServiceClient.from_connection_string(conn_str=CONNECTION_STRING)

# Checks to see if table exists and creates it if not True
def table_set_up():
    try:
        table_service.create_table(TABLE_NAME)
        return(f"Table '{TABLE_NAME}' created.")
    except ResourceExistsError:
        table_service.get_table_client(TABLE_NAME)
        return(f"Table '{TABLE_NAME}' already exists.")


def get_all_games():
    table_client = table_service.get_table_client(TABLE_NAME)

    # Query all entities in the table
    entities = table_client.list_entities()

    # Return a list of all entities
    return list(entities)

def save_to_table_storage(data):
    # Create a table service client
    
    # Get the table client
    table_client = table_service.get_table_client(TABLE_NAME)
    
    # Transform the game object into an entity
    entity = data
    # Insert or update the entity in the table
    table_client.upsert_entity(entity)
    print(f"Saved {entity['PartitionKey']} with RowKey {entity['RowKey']} to table {TABLE_NAME}")

def delete_game_by_id(game_id: int):

    # Create the table service client
    table_client = table_service.get_table_client(TABLE_NAME)

    # Query for the entity with the specified game_id
    filter_query = f"PartitionKey eq {game_id}"
    entities = table_client.query_entities(filter_query)

    # Iterate through entities to find the first match
    for entity in entities:
        partition_key = entity["PartitionKey"]
        row_key = entity["RowKey"]
        
        # Delete the entity
        table_client.delete_entity(partition_key=partition_key, row_key=row_key)
        print(f"Deleted game with id={game_id} from table {TABLE_NAME}.")
        return  # Exit after deleting the first match

    print(f"No game found with id={game_id} in table {TABLE_NAME}.")

def find_game_by_video_id_and_type(video_id: str, game_type: str):
    table_client = table_service.get_table_client(TABLE_NAME)

    # Query for the specific entity
    query_filter = f"PartitionKey eq '{video_id}' and RowKey eq '{game_type}'"
    entities = table_client.query_entities(query_filter)

    print("entity")
    for entity in entities:
        print(entity)
        return entity
    
    return None  # If no match found

def update_game_id(partition_key: str, row_key: str, new_game_id: int):
    table_client = table_service.get_table_client(TABLE_NAME)

    # Retrieve the entity
    entity = table_client.get_entity(partition_key=partition_key, row_key=row_key)
    
    # Update the `game_id` field
    entity["game_id"] = new_game_id
    
    # Upsert (update or insert) the entity back to the table
    table_client.upsert_entity(entity)
    print(f"Updated game_id to {new_game_id} for {partition_key} with RowKey {row_key}")
