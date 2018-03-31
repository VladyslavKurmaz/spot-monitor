#!/bin/bash -e
export $(cat ./../../.env | grep -v ^# | xargs)
docker run -d --rm -p ${SERVICES_SUSPICIOUS_PORT}:${SERVICES_SUSPICIOUS_PORT} --name spot-monitor-suspicious spot-monitor-suspicious
