#!/bin/bash

TZ_FILE="/usr/share/zoneinfo/$TZ"
LINK_DEST="/etc/localtime"

if [ -n "$TZ" ]; then
    ln -snf "$TZ_FILE" "$LINK_DEST"
    echo "Timezone link created: $TZ_FILE -> $LINK_DEST"
else
    echo "Running on default timezone UTC"
fi

mkdir -p /data/rubix-registry
echo "{\"_default\": {\"1\": {\"token\": \"$(eval echo "$@")\"}}}" > /data/rubix-registry/github_info.json
mkdir -p /data/systemd/system

# shellcheck disable=SC2016
echo '*/5 * * * * start_timestamp=$(systemctl show nubeio-rubix-bios.service --property=ExecMainStartTimestamp --value systemd); start_timestamp_seconds=$(date -d "$start_timestamp" +\%s); current_timestamp=$(date +\%s); elapsed_time=$((current_timestamp - start_timestamp_seconds)); [ "$elapsed_time" -gt 300 ] && (cp /lib/systemd/system/nubeio-* /data/systemd/system/ 2>/dev/null && echo "Executed systemd files copy command." || echo "No nubeio systemd files exists!") || echo "Skipped the systemd files copy!"' | crontab -
# shellcheck disable=SC2016
{ crontab -l; echo '*/5 * * * * start_timestamp=$(systemctl show nubeio-rubix-bios.service --property=ExecMainStartTimestamp --value systemd); start_timestamp_seconds=$(date -d "$start_timestamp" +\%s); current_timestamp=$(date +\%s); elapsed_time=$((current_timestamp - start_timestamp_seconds)); [ "$elapsed_time" -gt 300 ] && (cp /etc/openvpn/client.conf /data/openvpn 2>/dev/null && echo "Executed OpenVPN config copy command." || echo "No OpenVPN config exists!") || echo "Skipped the config backup!"'; } | crontab -

service cron start
exec /sbin/init
