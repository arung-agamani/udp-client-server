#!/bin/bash

if [ "${ROLE}" == 'receiver' ]
  then
    timeout 300 ./run_receiver.sh 1337
    sleep 5
  else
    timeout 300 ./run_sender.sh receiver_1,receiver_2 1337 $1
    sleep 5
fi
