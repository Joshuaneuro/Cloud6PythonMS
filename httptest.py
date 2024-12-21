GET http://192.168.2.12:5000/api/games

#####

GET http://192.168.2.12:5000/api/games/104/FindAllObjectsGame


######
POST http://192.168.2.12:5000/api/games
content-type: application/json

{
        "type": "MemoryGame",
        "id": 1,
        "videoId": 101,
        "imageUrls": ["https://example.com/image1.png", "https://example.com/image2.png"]
}

#####

POST http://192.168.2.12:5000/api/games
content-type: application/json

{
        "type": "FindAllObjects",
        "id": 4,
        "videoId": 104,
        "backgroundImageUrl": "https://example.com/background.png",
        "objects": [
            {"objectImageUrl": "https://example.com/object1.png", "x": 10, "y": 20},
            {"objectImageUrl": "https://example.com/object2.png", "x": 30, "y": 40}
        ]
    }

#####

POST http://192.168.2.12:5000/add
content-type: application/json

{
        "type": "PointAtPictureGame",
        "id": 3,
        "video_id": 103,
        "correct_image_url": "https://example.com/correct.png",
        "incorrect_images_urls": ["https://example.com/incorrect1.png", "https://example.com/incorrect2.png"],
        "sound_url": "https://example.com/sound.mp3"
}

#####
