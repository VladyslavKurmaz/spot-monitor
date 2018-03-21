#!/bin/bash -e
export $(cat ./../../.env | grep -v ^# | xargs)
docker stop spot-monitor-camera
docker rmi spot-monitor-camera
