#!/bin/bash -e
export $(cat ./../../.env | grep -v ^# | xargs)
echo "export const hosts = { cameraHost: 'http://${SERVICES_CAMERA_HOST}:${SERVICES_CAMERA_PORT}' };" > src/hosts.ts
ng build
ng serve --host 0.0.0.0 --port 4201
