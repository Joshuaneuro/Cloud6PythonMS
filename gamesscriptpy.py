from flask import Flask, jsonify, request
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)

# Azure Storage configuration
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
BLOB_SERVICE_CLIENT = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

@app.route('/list-blobs', methods=['GET'])
def list_blobs():
    container_name = request.args.get('container')
    
    if not container_name:
        return jsonify({"error": "Container name is required"}), 400

    try:
        container_client = BLOB_SERVICE_CLIENT.get_container_client(container_name)
        blobs = container_client.list_blobs()
        blob_list = [{"name": blob.name, "size": blob.size} for blob in blobs]

        return jsonify({"blobs": blob_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload-blob', methods=['POST'])
def upload_blob():
    container_name = request.form.get('container')
    file = request.files.get('file')

    if not container_name or not file:
        return jsonify({"error": "Container name and file are required"}), 400

    try:
        container_client = BLOB_SERVICE_CLIENT.get_container_client(container_name)
        blob_client = container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file, overwrite=True)

        return jsonify({"message": f"File {file.filename} uploaded successfully to container {container_name}."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
