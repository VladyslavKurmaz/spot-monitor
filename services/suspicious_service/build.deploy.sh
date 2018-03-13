#!/usr/bin/env bash

docker build -t ogvalt/warp_service:latest -f Dockerfile .

docker push ogvalt/warp_service:latest