GET http://192.168.2.12:5000/api/games

#####

GET http://192.168.2.12:5000/api/games/1/FindAllObjectsGame


######
POST http://192.168.2.12:5000/api/games
content-type: application/json

{
        "type": "memorygame",
        "id": 1,
        "videoId": 101,
        "imageUrls": ["https://example.com/image1.png", "https://example.com/image2.png"]
}

#####

POST http://192.168.2.12:5000/api/games
content-type: application/json

{
        "type": "findallobjects",
        "id": 1,
        "videoId": 101,
        "backgroundImageUrl": "https://example.com/background.png",
        "objects": [
            {"objectImageUrl": "https://example.com/object1.png", "x": 10, "y": 20},
            {"objectImageUrl": "https://example.com/object2.png", "x": 30, "y": 40}
        ]
    }

#####

POST http://192.168.2.12:5000/api/games
content-type: application/json

{
        "type": "PointAtPictureGame",
        "id": 1,
        "videoId": 101,
        "correctImageUrl": "https://example.com/correct.png",
        "incorrectImagesUrls": ["https://example.com/incorrect1.png", "https://example.com/incorrect2.png"],
        "soundUrl": "https://example.com/sound.mp3"
}

#####
