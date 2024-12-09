game = []
memorygame = []
objectgame = []
findobjectgame = []
pointatpicturegame = []

class Game:
    def __init__(self, id, videoId):
        self.id = id
        self.videoId = videoId

class MemoryGame:
    def __init__(self, id, videoId, imageUrls):
        self.id = id
        self.videoId = videoId
        #list
        self.imageUrls = imageUrls

class ObjectGame:
    def __init__(self,objectImageUrl, x, y):
        self.objectImageUrl = objectImageUrl
        self.x = x
        self.y = y

class FindObjectGame:
    def __init__(self, backgroundImageUrl, objects):
        self.backgroundImageUrl = backgroundImageUrl
        self.objects = objects

class PointAtPictureGame:
    def __init__(self, correctImageUrl, incorrectImageUrl, soundUrl, pointAtPictureGame):
        self.correctImageUrl = correctImageUrl
        #list
        self.incorrectImageUrl = incorrectImageUrl
        self.soundUrl = soundUrl
        #self refrence
        self.pointAtPictureGame = pointAtPictureGame