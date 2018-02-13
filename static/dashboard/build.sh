#!/bin/bash

export $(cat ./../../.env | grep -v ^# | xargs)
ng build
