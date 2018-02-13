#!/bin/bash

export $(cat ./../../.env | grep -v ^# | xargs)

docker run -d \
  -p $WEB_PORT:$WEB_PORT \
  -p $WEB_PORTS:$WEB_PORTS \
  -p $API_PORT:$API_PORT \
  --rm \
  --name com.attlas.lb com.attlas.lb