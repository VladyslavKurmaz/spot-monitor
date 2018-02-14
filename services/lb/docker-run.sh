#!/bin/bash

export $(cat ./../../.env | grep -v ^# | xargs)

docker run -d \
  -p $STATIC_DASHBOARD_PORT:$STATIC_DASHBOARD_PORT \
  -p $STATIC_DASHBOARD_PORTS:$STATIC_DASHBOARD_PORTS \
  -p $SERVICES_API_PORT:$SERVICES_API_PORT \
  --rm \
  --name com.globallogic.pocs.spotmonitor.lb com.globallogic.pocs.spotmonitor.lb