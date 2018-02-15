#!/bin/bash -xe

pushd services/api
./build.sh
popd

pushd static/dashboard
./build.sh
popd

