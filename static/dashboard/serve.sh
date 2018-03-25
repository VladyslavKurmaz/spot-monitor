#!/bin/bash -e
export $(cat ./../../.env | grep -v ^# | xargs)
envsubst < src/hosts.ts.template > src/hosts.ts
ng build
ng serve --host 0.0.0.0 --port 4201
