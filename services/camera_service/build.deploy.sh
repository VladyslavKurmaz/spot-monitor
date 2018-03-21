#!/usr/bin/env bash

docker build -t ogvalt/camera_server:latest -f Dockerfile .

docker push ogvalt/camera_server:latest