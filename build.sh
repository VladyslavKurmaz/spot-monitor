#!/bin/bash

pushd services/api
./build.sh
popd

pushd static/dashboard
./build.sh
popd

