#!/bin/bash
set -e

docker-compose -p $(cat .run_id) down > /dev/null
docker-compose rm -f > /dev/null

echo "success"