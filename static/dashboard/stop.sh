#!/bin/bash -e
export $(cat ./../../.env | grep -v ^# | xargs)
docker stop spot-monitor-dashboard
docker rmi spot-monitor-dashboard
