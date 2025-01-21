#! /usr/bin/env sh
set -e

python /app/manage.py migrate

exec "$@"

