#!/bin/bash -e

sudo apt-get update
sudo apt-get install -y jq

DEST=`sudo docker inspect cfy | jq -r '.[0].Volumes["/opt/influxdb/shared/data"]'`
sudo find $DEST -type f -delete
sudo docker exec cfy /usr/bin/pkill influxdb
sleep 10
curl --fail "http://localhost:8086/db?u=root&p=root" -d "{\"name\": \"cloudify\"}"
