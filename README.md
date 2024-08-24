# efk-stack-play
A play area for an EFK stack running locally.

The fluent-bit build involves building the vdisk fluent-bit plugin, and dropping it into a fluent-bit image.

The stack can be brought up with
```
docker compose up --build
```

Elasticsearch and Kibana are available on their usual ports; `http://localhost:9200` and `http://localhost:5601` respectively.

The Elastic stack has an APM server, available on `http://localhost:8200`. Using APM with Elastic requires using Fleet, which means turning on xpack security. There is a fair bit of extra red-tape involved in setting up all the usernames and passwords for the various system roles. The admin role has the password `changeme` set at start up. The rest of the roles are configured in a setup sidecar, which assigns the password `changeme` to the roles `elastic remote_monitoring_user beats_system logstash_system kibana kibana_system apm_system`. Handling passwords open, checked into code, and over http (i.e. without TLS) is NOT OK for production; only here for test purposes. The password is liberally written, unecrypted, in various areas; to see all the places grep for `changeme`.