#!/bin/bash -e
export $(cat ./../../.env | grep -v ^# | xargs)
docker run -d --rm -p ${SERVICES_NEURAL_PORT}:${SERVICES_NEURAL_PORT} --name spot-monitor-neural spot-monitor-neural
