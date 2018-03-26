#!/bin/bash -e
export $(cat ./../../.env | grep -v ^# | xargs)
docker run -d --rm -p ${STATIC_DASHBOARD_PORT}:${STATIC_DASHBOARD_PORT} --name spot-monitor-dashboard spot-monitor-dashboard
