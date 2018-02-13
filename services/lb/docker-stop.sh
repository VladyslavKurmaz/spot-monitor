#!/bin/bash

export $(cat ./../../.env | grep -v ^# | xargs)

docker stop com.attlas.lb
docker rmi com.attlas.lb
