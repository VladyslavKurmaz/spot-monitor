#!/bin/bash -e
export $(cat ./../../.env | grep -v ^# | xargs)
docker run -d --rm -p ${SERVICES_CAMERA_PORT}:${SERVICES_CAMERA_PORT} --name spot-monitor-camera spot-monitor-camera
