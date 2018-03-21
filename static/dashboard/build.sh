#!/bin/bash -e
export $(cat ./../../.env | grep -v ^# | xargs)
ng build --prod --env=prod
docker build -t spot-monitor-dashboard .
