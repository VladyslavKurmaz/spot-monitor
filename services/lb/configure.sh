#!/bin/bash

sed -i "s/%WORKER_PROCESSES%/$LB_STATIC_WEB_NUM/" /nginx.conf
sed -i "s/%WEB_PORT%/$WEB_PORT/" /nginx.conf
sed -i "s/%API_PORT%/$API_PORT/" /nginx.conf

STATIC_SERVERS=''
for i in $(seq 1 $LB_STATIC_WEB_NUM)
do
  STATIC_SERVERS="$STATIC_SERVERS\nserver ${COMPOSE_PROJECT_NAME}_${LB_STATIC_WEB_NAME}_$i:${WEB_PORT};"
done
sed -i "s/%STATIC_SERVERS%/$STATIC_SERVERS/" /nginx.conf

SERVICE_SERVERS=''
for i in $(seq 1 $LB_SERVICES_API_NUM)
do
  SERVICE_SERVERS="$SERVICE_SERVERS\nserver ${COMPOSE_PROJECT_NAME}_${LB_SERVICES_API_NAME}_$i:${API_PORT};"
done
sed -i "s/%SERVICE_SERVERS%/$SERVICE_SERVERS/" /nginx.conf
