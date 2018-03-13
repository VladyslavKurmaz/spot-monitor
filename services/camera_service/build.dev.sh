#!/usr/bin/env bash

docker build -t ogvalt/camera_server:dev -f Dockerfile.dev .

docker push ogvalt/camera_server:dev