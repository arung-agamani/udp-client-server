#!/bin/bash

# Panggil program anda untuk mode siap mengirim file
# $1 berisi address receiver (akan diisi oleh autograder)
# $2 berisi port receiver (akan diisi oleh autograder)
# $3 berisi path file yang akan dikirim (akan diisi oleh autograder)
# Contoh: echo -e "$1\n$2\n$3" | python3 sender.py

echo -e "127.0.0.1\n9999\ntest.txt"
