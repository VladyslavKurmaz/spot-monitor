# Camera service

## Deployment

Here will be some information about deployment of this thing

## API

Get list of all cameras
    
    GET http://example.com/cameras

    response = {
        "data": [
            {
                "endpoint": "http://0.0.0.0:8001/suspicious/1",
                "health": true,
                "id": 1,
                "video_source": "172.22.61.80:554",
                "stream_url": "http://0.0.0.0:8001/suspicious/1"
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
                "endpoint": "http://0.0.0.0:8001/suspicious/1",
                "health": true,
                "id": 1,
                "video_source": "172.22.61.80:554",
                "stream_url": "http://0.0.0.0:8001/suspicious/1"
            }
        ],
        "message": "Success",
        "status": true
    }
    
Add new camera

    POST http://example.com/cameras
    
    request = {
        "ip": "172.22.61.80:554",
        "user": "admin",
        "password": "admin123",
        "endpoint": "http://0.0.0.0:8001/suspicious"
    }

    response = {
        "data": [
            {
                "endpoint": "http://0.0.0.0:8001/suspicious/2",
                "health": true,
                "id": 2,
                "stream_url": null,
                "video_source": "172.22.61.80:554"
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
                "endpoint": "http://0.0.0.0:8001/suspicious/2",
                "health": true,
                "id": 2,
                "stream_url": null,
                "video_source": "172.22.61.80:554"
            }
        ],
        "message": "Deleted",
        "status": true
    }
    
Get stream from camera

    GET http://example.com/stream/<int-id>
    
    responce.mimetype='multipart/x-mixed-replace; boundary=frame'