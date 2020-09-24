#!/bin/bash
set -e

source grading_helper.sh

set_tc disable

docker exec "$(cat .run_id)_sender_1" ping -c 1 receiver_1 > /dev/null
docker exec "$(cat .run_id)_sender_1" ping -c 1 receiver_2 > /dev/null

echo "success"