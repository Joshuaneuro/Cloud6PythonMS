GET http://192.168.2.12:5000/list

#####

POST http://192.168.2.12:5000/api/games
content-type: application/json

{
    "id": 4,
    "videoId": 100004
}

######
POST http://192.168.2.12:5000/add
content-type: application/json

{
    "PartitionKey": "samplePartition",
    "RowKey": "sampleRow5",
    "id": 5,
    "videoId": 1000005,
    "memoryGame": {
        "id": 5,
        "videoId": 100005,
        "imageUrls": "urlforimage.jpg"
    },
    "objectGame": {
        "objectImageUrl": "urlforobject.jpg",
        "x": "xcordinates",
        "y": "ycordinates"
    },
    "findObjectGame": {
        "backgroundImageUrl": "urlforbackground.jpg",
        "objects": "object"
    },
    "pointAtPictureGame": {
        "correctImageUrl": "urlforcorrectimage.jpg",
        "inccorectimageurl": {
            "imageurl": "urlforimage"
        },
        "soundUrl": "urlforsound.mov"
    }
}