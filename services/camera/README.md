# Camera service

## Deployment

Here will be some information about deployment of this thing

## API

Naming convention in responce's "data" field


    responce = {
        "data": [
            {
                "id": <int> - unique camera identifier
                "health": <bool> - stream health
                "cameraIPAddress": <string> - IP address of the camera  
                "username": <string> - stream access username
                "password": <string> - stream access password
                "streamDestination": <string> - where camera instance send it's stream
                "streamUrl": <string> - access to stream
            }
        ],
        ...
    }

Get list of all cameras
    
    GET http://example.com/cameras

    response = {
        "data": [
            {
                "id": <int> - unique camera identifier
                "health": <bool> - stream health
                "cameraIPAddress": <string> - IP address of the camera  
                "username": <string> - stream access username
                "password": <string> - stream access password
                "streamDestination": <string> - where camera instance send it's stream
                "streamUrl": <string> - access to stream
            }
        ],
        "message": "Success",
        "status": true
    }

Get specific camera

    GET http://example.com/cameras/<int-id>

    response = {
        "data": [
            {
                "id": <int> - unique camera identifier
                "health": <bool> - stream health
                "cameraIPAddress": <string> - IP address of the camera  
                "username": <string> - stream access username
                "password": <string> - stream access password
                "streamDestination": <string> - where camera instance send it's stream
                "streamUrl": <string> - access to stream
            }
        ],
        "message": "Success",
        "status": true
    }
    
Add new camera

    POST http://example.com/cameras
    
    request = {
        "ip": "172.22.61.80",
        "user": "admin",
        "password": "admin123",
        "endpoint": "http://0.0.0.0:8001/suspicious"
    }

    response = {
        "data": [
            {
                "id": <int> - unique camera identifier
                "health": <bool> - stream health
                "cameraIPAddress": <string> - IP address of the camera  
                "username": <string> - stream access username
                "password": <string> - stream access password
                "streamDestination": <string> - where camera instance send it's stream
                "streamUrl": <string> - access to stream
            }
        ],
    "message": "Camera added",
    "status": true
    }
    
Delete camera

    DELETE http://example.com/cameras/<int-id>
    
    responce = {
        "data": [
            {
                "id": <int> - unique camera identifier
                "health": <bool> - stream health
                "cameraIPAddress": <string> - IP address of the camera  
                "username": <string> - stream access username
                "password": <string> - stream access password
                "streamDestination": <string> - where camera instance send it's stream
                "streamUrl": <string> - access to stream
            }
        ],
        "message": "Deleted",
        "status": true
    }
    
Get stream from camera

    GET http://example.com/stream/<int-id>
    
    responce.mimetype='multipart/x-mixed-replace; boundary=frame'