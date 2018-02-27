#!/bin/bash -e
DIR=$(dirname "$(readlink -f "$0")")
docker run --rm -v $DIR:$DIR maven:3.5-jdk-8 mvn -f $DIR clean install
