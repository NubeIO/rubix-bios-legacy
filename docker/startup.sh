#!/bin/bash

mkdir -p /data/rubix-registry
echo {\"_default\": {\"1\": {\"token\": \"$(eval echo "$@")\"}}} > /data/rubix-registry/github_info.json
mkdir -p /data/systemd/system
crontab -l
echo "* * * * * cp /lib/systemd/system/nubeio-* /data/systemd/system/ 2>/dev/null || echo \"No nubeio systemd files exists\!\" && echo \"Executed copy command.\"" | crontab -
service cron start
exec /sbin/init
