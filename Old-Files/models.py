class Game:
    def __init__(self, id, videoId):
        self.id = id
        self.videoId = videoId

class MemoryGame(Game):
    def __init__(self, id, videoId, imageUrls):
        super().__init__(id, videoId)
        self.imageUrls = imageUrls
    def __repr__(self):
        return (
            f"MemoryGame(id={self.id}, videoId={self.videoId}, "
            f"imageUrls={self.imageUrls})"
        )
    
class ObjectPlacement():
    def __init__(self,objectImageUrl, x, y):
        self.objectImageUrl = objectImageUrl
        self.x = x
        self.y = y
    def __repr__(self):
        return f"ObjectPlacement(objectImageUrl='{self.objectImageUrl}', x={self.x}, y={self.y})"

class FindAllObjectsGame(Game):
    def __init__(self,id ,videoId,backgroundImageUrl, objects):
        super().__init__(id,videoId)
        self.backgroundImageUrl = backgroundImageUrl
        self.objects = objects
    def __repr__(self):
        return (
            f"FindAllObjects(id={self.id}, videoId={self.videoId}, "
            f"backgroundImageUrl='{self.backgroundImageUrl}', objects={self.objects})"
        )

class PointAtPictureGame(Game):
    def __init__(self,id,videoId ,correctImageUrl, incorrectImageUrls, soundUrl):
        super().__init__(id,videoId)
        self.correctImageUrl = correctImageUrl        
        self.incorrectImageUrls = incorrectImageUrls
        self.soundUrl = soundUrl
    def __repr__(self):
        return (
            f"PointAtPictureGame(id={self.id}, videoId={self.videoId}, "
            f"correctImageUrl='{self.correctImageUrl}', "
            f"incorrectImagesUrls={self.incorrectImageUrls}, "
            f"soundUrl='{self.soundUrl}')"
        )