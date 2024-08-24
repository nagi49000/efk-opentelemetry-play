# efk-opentelemtry-play
A play area for an EFK stack running locally using opentelemetry for sending logs, metrics and traces.

The stack can be brought up with
```
docker compose up --build
```

Elasticsearch and Kibana are available on their usual ports; `http://localhost:9200` and `http://localhost:5601` respectively.

The Elastic stack has an APM server, available on `http://localhost:8200`. Using APM with Elastic requires using Fleet, which means turning on xpack security. There is a fair bit of extra red-tape involved in setting up all the usernames and passwords for the various system roles. The admin role has the password `changeme` set at start up. The rest of the roles are configured in a setup sidecar, which assigns the password `changeme` to the roles `elastic remote_monitoring_user beats_system logstash_system kibana kibana_system apm_system`. Handling passwords open, checked into code, and over http (i.e. without TLS) is NOT OK for production; only here for test purposes. The password is liberally written, unecrypted, in various areas; to see all the places grep for `changeme`.

The APM integration will create a data view called 'APM', which can be used directly in discover, or in any dashboarding. This data view gives a view on all of the traces, metrics and logs uploaded from the APM server.

### Observability - alerts

With metrics and logs going into Elastic's APM via Opentelemetry, one can configure alerts in Elastic. From the main hamburger icon in the top left of Kibana, one can use the left hand menu to go to Observability > Alerts. One can then create a Rule (from 'Manage Rules', probably a 'custom threshold' rule) which can then be used for monitoring and issuing alerts.