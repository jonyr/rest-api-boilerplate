#!/bin/bash
set -e

if [[ $1 == 'api' ]] ; then
  echo "Running database migrations"
  flask db upgrade
  gunicorn -c ./src/config/gunicorn.py wsgi:app
  exit 0
fi

exec "$@"
