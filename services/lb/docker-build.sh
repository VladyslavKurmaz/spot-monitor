#!/bin/bash

export $(cat ./../../.env | grep -v ^# | xargs)

docker build -t com.globallogic.pocs.spotmonitor.lb \
    --build-arg COMPOSE_PROJECT_NAME=$COMPOSE_PROJECT_NAME \
    --build-arg LB_STATIC_DASHBOARD_NAME=$LB_STATIC_DASHBOARD_NAME \
    --build-arg LB_STATIC_DASHBOARD_NUM=$LB_STATIC_DASHBOARD_NUM \
    --build-arg LB_SERVICES_API_NAME=$LB_SERVICES_API_NAME \
    --build-arg LB_SERVICES_API_NUM=$LB_SERVICES_API_NUM \
    --build-arg STATIC_DASHBOARD_PORT=$STATIC_DASHBOARD_PORT \
    --build-arg STATIC_DASHBOARD_PORTS=$STATIC_DASHBOARD_PORTS \
    --build-arg SERVICES_API_PORT=$SERVICES_API_PORT \
    .
