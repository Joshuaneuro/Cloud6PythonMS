class Game:
    def __init__(self, id, videoId, blob_url, blob_name, metadata=None):
        self.id = id
        self.videoId = videoId
        self.blob_url = blob_url
        self.blob_name = blob_name
        self.metadata = metadata or {}