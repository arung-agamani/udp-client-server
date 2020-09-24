#!/bin/bash

# Change directory to this script location

[ ! -f .run_id ] && uuidgen | sed 's/-//g' > .run_id
cp -f .run_id .github/tests/.run_id

mkdir -p out_1
mkdir -p out_2

cp -r .github/tests/* .

docker-compose -p $(cat .run_id) up -d