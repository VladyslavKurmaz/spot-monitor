#!/bin/bash -e
export $(cat ./../../.env | grep -v ^# | xargs)
envsubst < src/hosts.ts.template > src/hosts.ts
ng build --prod --env=prod
docker build -t spot-monitor-dashboard .
