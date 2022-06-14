#!/bin/bash

echo "STOPPING CONTAINERS"
docker stop $(docker ps -a -q)

echo "REBUILD IMAGES"
sleep 1
#docker compose -f docker-compose.yml -f docker-compose.ci.yml build
echo "... or not"

echo "RECREATE DB"
sleep 1
docker compose -f docker-compose.yml  up  --force-recreate -V -d database

echo "RUN TESTS (first test can take a while - it has to wait for dask worker to start)"
sleep 1
# --wait-for-client
docker compose -f docker-compose.yml run backend poetry run pytest -v --forked --numprocesses=1
pytest_units_status=$?
