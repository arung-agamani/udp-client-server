#!/bin/bash

function set_tc {
  docker exec "$(cat .run_id)_sender_1" /usr/app/.github/tests/set_tc.sh $1
  docker exec "$(cat .run_id)_receiver_1_1" /usr/app/.github/tests/set_tc.sh $1
  docker exec "$(cat .run_id)_receiver_2_1" /usr/app/.github/tests/set_tc.sh $1
}