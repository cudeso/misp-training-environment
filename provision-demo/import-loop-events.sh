#!/usr/bin/bash

PAUSE_BETWEEN_EVENTS=1m
BASE_PATH="/home/ubuntu/provision-demo"

echo "Remember to run this script through screen!"
echo "-------------------------------------------"
echo " "

for FILE in $BASE_PATH/misp-events/*.json ; do date && echo Process $FILE && $BASE_PATH/import-event.py -i $FILE && sleep $PAUSE_BETWEEN_EVENTS; done

