#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Usage: $0 start|stop"
  echo "Examples:"
  echo "----------------------------------------------"
  echo " ./manager.sh start: starts all the containers"
  echo " ./manager.sh stop: stops all the containers"
  exit 1
fi

if [ "$1" == "start" ]; then
  docker-compose -f docker-compose.yml --env-file ./instance/.env up -d --build --remove-orphans
elif [ "$1" == "stop" ]; then
  docker-compose -f docker-compose.yml --env-file ./instance/.env down
else
  echo "Error: Invalid argument $1"
  echo "Usage: $0 start|stop"
  exit 1
fi



