#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Usage: $0 start|stop|fullstart|fullstop|fullconfig"
  echo "Examples:"
  echo "----------------------------------------------"
  echo " ./manager.sh start: starts all the containers without redis and postgres"
  echo " ./manager.sh stop: stops all the containers"
  echo " ./manager.sh fullstart: starts all the containers with redis and postgres"
  echo " ./manager.sh fullstop: stops all the containers"
  echo " ./manager.sh fullconfig: shows the overrided configuration"
  exit 1
fi

if [ "$1" == "start" ]; then
  docker-compose -f docker-compose.yml --verbose --env-file ./instance/.env up -d --build  --remove-orphans
elif [ "$1" == "stop" ]; then
  docker-compose -f docker-compose.yml --env-file ./instance/.env down
elif [ "$1" == "fullstart" ]; then
  docker-compose -f docker-compose.yml -f docker-compose-override.yml --env-file ./instance/.env down
elif [ "$1" == "fullstop" ]; then
  docker-compose -f docker-compose.yml -f docker-compose-override.yml --env-file ./instance/.env down
elif [ "$1" == "fullconfig" ]; then
  docker-compose -f docker-compose.yml -f docker-compose-override.yml --env-file ./instance/.env config
else
  echo "Error: Invalid argument $1"
  echo "Usage: $0 start|stop"
  exit 1
fi



