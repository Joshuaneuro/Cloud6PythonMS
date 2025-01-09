from Domain.Game import Game

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
