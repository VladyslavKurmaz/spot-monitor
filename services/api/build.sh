#!/bin/bash

export $(cat ./../../.env | grep -v ^# | xargs)
mvn clean install
