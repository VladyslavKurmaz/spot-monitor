#!/usr/bin/env bash

gunicorn -c ./gunicorn.conf wsgi:app