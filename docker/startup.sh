#!/bin/bash
setsid ./rubix-bios -p 1615 -g /data/rubix-bios -d data -c config -a apps --prod --auth --device-type amd64 --token $(eval echo "$@") > output.txt &
exec /sbin/init
