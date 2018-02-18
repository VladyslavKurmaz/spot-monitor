#!/bin/bash -e
DIR=$(dirname "$(readlink -f "$0")")
mvn clean install
