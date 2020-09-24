#!/bin/bash
set -e
source grading_helper.sh

if [ ! -f ./run_receiver.sh ] || [ ! -f ./run_sender.sh ]
  then
    echo 'fail: run_receiver.sh atau run_sender.sh tidak ada'
    exit 1
fi

set_tc $2

if [ $1 == "easy" ]
then
  for FILE in ./in/*.easy.txt
  do
    docker exec "$(cat .run_id)_receiver_1_1" ./runs/single.sh $FILE &
    PRCV=$!
    docker exec "$(cat .run_id)_sender_1" ./runs/single.sh $FILE &
    PSEND=$!
    wait $PRCV $PSEND

    if [ ! -f ./out_1/downloaded ]
      then
        echo 'fail: ./out_1/downloaded tidak ada'
        exit 1
    fi

    MD5_SUM_IN=$(md5sum $FILE | sed 's/\W.*//') 
    MD5_SUM_OUT=$(md5sum ./out_1/downloaded | sed 's/\W.*//') 

    rm -f ./out_1/downloaded

    if [ $MD5_SUM_IN != $MD5_SUM_OUT ]
    then
        echo 'fail: md5sum tidak sama'
        exit 1
    fi
  done
elif [ $1 == "medium" ]
then
  for FILE in ./in/*.medium.txt
  do
    docker exec "$(cat .run_id)_receiver_1_1" ./runs/single.sh $FILE &
    PRCV=$!
    docker exec "$(cat .run_id)_sender_1" ./runs/single.sh $FILE &
    PSEND=$!
    wait $PRCV $PSEND

    if [ ! -f ./out_1/downloaded ]
      then
        echo 'fail: ./out_1/downloaded tidak ada'
        exit 1
    fi

    MD5_SUM_IN=$(md5sum $FILE | sed 's/\W.*//') 
    MD5_SUM_OUT=$(md5sum ./out_1/downloaded | sed 's/\W.*//') 

    rm -f ./out_1/downloaded

    if [ $MD5_SUM_IN != $MD5_SUM_OUT ]
    then
        echo 'fail: md5sum tidak sama'
        exit 1
    fi
  done
else
  for FILE in ./in/*.easy.txt
  do
    docker exec "$(cat .run_id)_receiver_1_1" ./runs/multiple.sh $FILE &
    PRCV1=$!
    docker exec "$(cat .run_id)_receiver_2_1" ./runs/multiple.sh $FILE &
    PRCV2=$!
    docker exec "$(cat .run_id)_sender_1" ./runs/multiple.sh $FILE &
    PSEND=$!
    wait $PRCV1 $PRCV2 $PSEND

    if [ ! -f ./out_1/downloaded ] || [ ! -f ./out_2/downloaded ]
      then
        echo 'fail: ./out_1/downloaded atau ./out_2/downloaded  tidak ada'
        exit 1
    fi

    MD5_SUM_IN=$(md5sum $FILE | sed 's/\W.*//') 
    MD5_SUM_OUT1=$(md5sum ./out_1/downloaded | sed 's/\W.*//') 
    MD5_SUM_OUT2=$(md5sum ./out_2/downloaded | sed 's/\W.*//') 

    rm -f ./out_1/downloaded
    rm -f ./out_2/downloaded

    if [ $MD5_SUM_IN != $MD5_SUM_OUT1 ] || [ $MD5_SUM_IN != $MD5_SUM_OUT2 ]
    then
        echo 'fail: md5sum tidak sama'
        exit 1
    fi
  done
fi

exit 0
