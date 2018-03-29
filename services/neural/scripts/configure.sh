#!/bin/bash

_term() {
  echo "Caught SIGTERM signal!"
  kill -2 "$child" 2>/dev/null
}

cd ./app/api/src/libs/
sh init.sh

trap _term SIGINT

cd /scripts/
gunicorn -c ./gunicorn.conf wsgi:app &

child=$!
wait "$child"