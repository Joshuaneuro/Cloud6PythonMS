from Domain.Game import Game

class MemoryGame(Game):
    def __init__(self, id, videoId, imageUrls):
        super().__init__(id, videoId)
        self.imageUrls = imageUrls
    def __repr__(self):
        return (
            f"MemoryGame(id={self.id}, videoId={self.videoId}, "
            f"imageUrls={self.imageUrls})"
        )