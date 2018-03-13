#!/usr/bin/env bash

docker build -t ogvalt/neural:latest -f Dockerfile .

docker push ogvalt/neural:latest