#!/bin/bash -e
export $(cat ./../../.env | grep -v ^# | xargs)
docker stop spot-monitor-neural
docker rmi spot-monitor-neural
