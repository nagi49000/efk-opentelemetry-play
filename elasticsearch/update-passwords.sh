#!/bin/bash
set -eux

usernames=( elastic remote_monitoring_user beats_system logstash_system kibana kibana_system apm_system )
for key in "${usernames[@]}"
do
    cat pw.txt | elasticsearch-reset-password --url http://elasticsearch:9200 --verbose --force --interactive --username ${key}
done
