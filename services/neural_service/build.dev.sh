#!/usr/bin/env bash

docker build -t ogvalt/neural:dev -f Dockerfile.dev .

docker push ogvalt/neural:dev