#!/usr/bin/env bash

docker build -t ogvalt/warp_service:dev -f Dockerfile .

docker push ogvalt/warp_service:dev