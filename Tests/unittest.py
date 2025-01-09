import unittest
from unittest.mock import MagicMock, patch
from azure.data.tables import TableServiceClient

class TestAzureTableStorageQuery(unittest.TestCase):
    def setUp(self):
        # Mock connection string and table name
        self.connection_string = "FakeConnectionString"
        self.table_name = "TestTable"
        
        # Mock table client
        self.table_service_mock = MagicMock(spec=TableServiceClient)
        self.table_client_mock = self.table_service_mock.get_table_client.return_value

        # Example data in Azure Table Storage
        self.example_data = [
            {
                "PartitionKey": "1",
                "RowKey": "FindAllObjectsGame",
                "backgroundImageUrl": "https://example.com/background.png",
                "objects": "https://example.com/object1.png:10:20,https://example.com/object2.png:30:40",
                "videoId": 101
            },
            {
                "PartitionKey": "1",
                "RowKey": "MemoryGame",
                "imageUrls": "https://example.com/image1.png,https://example.com/image2.png",
                "videoId": 101
            },
            {
                "PartitionKey": "1",
                "RowKey": "PointAtPictureGame",
                "correctImageUrl": "https://example.com/correct.png",
                "incorrectImagesUrls": "https://example.com/incorrect1.png,https://example.com/incorrect2.png",
                "soundUrl": "https://example.com/sound.mp3",
                "videoId": 101
            },
        ]

    @patch("azure.data.tables.TableServiceClient")
    def test_query_entity_by_partition_and_row_key(self, mock_table_service_client):
        # Mock TableServiceClient to return the mocked table client
        mock_table_service_client.from_connection_string.return_value = self.table_service_mock
        
        # Mock query_entities response
        self.table_client_mock.query_entities.return_value = [
            self.example_data[1]  # MemoryGame entity
        ]

        # Perform the query
        partition_key = "1"
        row_key = "MemoryGame"
        query_filter = f"PartitionKey eq '{partition_key}' and RowKey eq '{row_key}'"

        # Call the function to query
        table_service = TableServiceClient.from_connection_string(self.connection_string)
        table_client = table_service.get_table_client(self.table_name)
        entities = table_client.query_entities(query_filter)

        # Verify the result
        entities = list(entities)  # Convert to list to iterate
        self.assertEqual(len(entities), 1)
        self.assertEqual(entities[0]["PartitionKey"], "1")
        self.assertEqual(entities[0]["RowKey"], "MemoryGame")
        self.assertEqual(entities[0]["imageUrls"], "https://example.com/image1.png,https://example.com/image2.png")

    @patch("azure.data.tables.TableServiceClient")
    def test_query_all_entities_in_partition(self, mock_table_service_client):
        # Mock TableServiceClient to return the mocked table client
        mock_table_service_client.from_connection_string.return_value = self.table_service_mock

        # Mock query_entities response
        self.table_client_mock.query_entities.return_value = self.example_data

        # Perform the query
        partition_key = "1"
        query_filter = f"PartitionKey eq '{partition_key}'"

        # Call the function to query
        table_service = TableServiceClient.from_connection_string(self.connection_string)
        table_client = table_service.get_table_client(self.table_name)
        entities = table_client.query_entities(query_filter)

        # Verify the result
        entities = list(entities)  # Convert to list to iterate
        self.assertEqual(len(entities), 3)  # 3 entities in partition 1
        self.assertEqual(entities[0]["RowKey"], "FindAllObjectsGame")
        self.assertEqual(entities[1]["RowKey"], "MemoryGame")
        self.assertEqual(entities[2]["RowKey"], "PointAtPictureGame")

if __name__ == "__main__":
    unittest.main()
