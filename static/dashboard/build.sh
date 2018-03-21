#!/bin/bash -e
export $(cat ./../../.env | grep -v ^# | xargs)
echo "export const hosts = { cameraHost: 'http://${SERVICES_CAMERA_HOST}:${SERVICES_CAMERA_PORT}' };" > src/hosts.ts
ng build --prod --env=prod
docker build -t spot-monitor-dashboard .
