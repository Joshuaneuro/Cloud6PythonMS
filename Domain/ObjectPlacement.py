class ObjectPlacement():
    def __init__(self,objectImageUrl, x, y):
        self.objectImageUrl = objectImageUrl
        self.x = x
        self.y = y
    def __repr__(self):
        return f"ObjectPlacement(objectImageUrl='{self.objectImageUrl}', x={self.x}, y={self.y})"
