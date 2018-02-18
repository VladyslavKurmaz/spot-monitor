#!/bin/bash -e

DIR=$(dirname "$(readlink -f "$0")")
mvn -f api clean install
