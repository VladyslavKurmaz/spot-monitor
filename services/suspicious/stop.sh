#!/bin/bash -e
export $(cat ./../../.env | grep -v ^# | xargs)
docker stop spot-monitor-suspicious
docker rmi spot-monitor-suspicious
