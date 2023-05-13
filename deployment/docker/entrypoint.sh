#!/bin/bash
set -e

# Running the flask backend using gunicorn
if [[ $1 == 'api' ]] ; then
  echo "Running database migrations"
  flask db upgrade
  gunicorn -c ./src/config/gunicorn.py wsgi:app
  exit 0
fi

# Running the celery worker
if [[ $1 == 'worker' ]] ; then
  echo "Running celery worker"
  celery -A wsgi:celery worker --loglevel=info
  exit 0
fi

# Running the celery beat
if [[ $1 == 'beat' ]] ; then
  echo "Running celery beat"
  celery -A wsgi:celery beat --loglevel=info
  exit 0
fi

# Running the celery flower
if [[ $1 == 'flower' ]] ; then
  echo "Running celery flower"
  celery -A wsgi:celery flower --loglevel=info --port=5555
  exit 0
fi

exec "$@"
