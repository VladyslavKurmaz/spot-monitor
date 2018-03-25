#!/bin/bash -e
export $(cat ./../../.env | grep -v ^# | xargs)
docker build -t spot-monitor-neural .
