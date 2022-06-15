#!/bin/bash

echo "STOPPING CONTAINERS"
docker stop $(docker ps -a -q)

echo "REBUILD IMAGES"
sleep 1
#docker compose -f docker-compose.yml -f docker-compose.ci.yml build
echo "... or not"

sleep 1
# --wait-for-client
docker compose run backend poetry run pytest -v --forked --numprocesses=1
pytest_units_status=$?
