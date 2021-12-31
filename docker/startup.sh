#!/bin/bash

mkdir -p /data/rubix-registry
echo {\"_default\": {\"1\": {\"token\": \"$(eval echo "$@")\"}}} > /data/rubix-registry/github_info.json
exec /sbin/init