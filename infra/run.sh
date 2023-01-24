#!/bin/bash

set -exo pipefail

echo "Waiting for Postgres..."

while ! nc -z postgres 5432; do
	sleep 0.1
done

echo "Postgres started"

if [[ -z ${DEVELOPMENT} ]];then

    COMMAND=("$(which gunicorn)" "-k" "uvicorn.workers.UvicornWorker" "--preload" "--reuse-port" "--chdir=/code" "-b 0.0.0.0:${PORT:-8000}" "--max-requests=10000" "--max-requests-jitter=500" "-t" "60" "--graceful-timeout=30" "--keep-alive=2" "esorcerer.app:app")

else

    COMMAND=("$(which uvicorn)" "esorcerer.app:app" "--reload" "--workers" "1" "--host" "0.0.0.0" "--port" "${PORT:-8000}")

fi

exec "${COMMAND[@]}"
