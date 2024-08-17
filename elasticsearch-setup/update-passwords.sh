#!/bin/bash
set -eux

usernames=( elastic remote_monitoring_user beats_system logstash_system kibana kibana_system apm_system )
for key in "${usernames[@]}"
do
  echo "Updating password for user " ${key}
  curl -XPOST --header "Content-Type: application/json" --user elastic:changeme http://elasticsearch:9200/_security/user/${key}/_password --data '{"password":"changeme"}'
done
