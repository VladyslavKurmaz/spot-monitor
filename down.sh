#!/bin/bash

export $(cat ./.env | grep -v ^# | xargs)
docker-compose down --rmi all
