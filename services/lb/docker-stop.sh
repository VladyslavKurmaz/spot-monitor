#!/bin/bash

export $(cat ./../../.env | grep -v ^# | xargs)

docker stop com.globallogic.pocs.spotmonitor.lb
docker rmi com.globallogic.pocs.spotmonitor.lb
