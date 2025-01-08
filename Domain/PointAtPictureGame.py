from Game import Game

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