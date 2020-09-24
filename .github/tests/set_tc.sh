#!/bin/bash

if tc qdisc show dev eth0 | grep -q 'netem'
then
  tc qdisc del dev eth0 root
fi

if [ -z "$1" ] || [ $1 == "easy" ]
then
  tc qdisc add dev eth0 root netem delay 100ms 50ms reorder 5% corrupt 2% duplicate 1% loss 2%
elif [ $1 == "hard" ]
then
  tc qdisc add dev eth0 root netem delay 100ms 50ms reorder 8% corrupt 3% duplicate 1% loss 5%
fi