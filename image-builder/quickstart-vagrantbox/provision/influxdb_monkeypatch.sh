#!/bin/bash -e

apt-get update
apt-get install -y jq

DEST=`docker inspect cfy | jq -r '.[0].Volumes["/opt/influxdb/shared/data"]'`
rm -r $DEST/*
docker exec cfy /usr/bin/pkill influxdb
curl --fail "http://localhost:8086/db?u=root&p=root" -d "{\"name\": \"cloudify\"}"
