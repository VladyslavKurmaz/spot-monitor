# Camera service

## Deployment

Here will be some information about deployment of this thing

## API

Get suspicious regions for all cameras
    
    GET http://example.com/suspicious

    response = {
        "data": [
            {
                "1": null
            },
            {
                "2": null
            }
        ],
        "message": "All suspicious regions",
        "status": true
    }

Get suspicious regions for specific camera

    GET http://example.com/suspicious/<int-id>

    response = {
        "data": [
            {
                "1": null
            }
        ],
        "message": "Suspicious regions",
        "status": true
    }
    
Create suspicious monitor 

    POST http://example.com/suspicious
    
    request = {
        "cam_id": 1
    }

    response = {
        'status': True, 
        'message': 'Monitor created', 
        'data': [
            {
                'endpoint': '/1'
            }
        ]
    }
    
Send frame for processing

    POST http://example.com/suspicious/<int-id>
    
    request.headers={'content-type': 'image/jpeg'}

    response = {
        'status': True, 
        'message': 'Processed', 
        'data': [
            {
                suspicious regions
            }
        ]
    }
    
Delete monitor

    DELETE http://example.com/suspicious/<int-id>
    
    response = {
        'status': True, 
        'message': 'Monitor deleted', 
        'data': [
            {
                'id': <identifier>
            }
        ]
    }