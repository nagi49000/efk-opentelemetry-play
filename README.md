# efk-opentelemtry-play
A play area for an EFK stack running locally using opentelemetry for sending logs, metrics and traces.

The descriptions for Opentelemetry and implementations can be rather obtuse. The motivation is a vendor-agnostic way of handling traces in a centralised manner (which then also allows centralised logs and metrics as a small piggy back). The abstract model (abstract in the sense that no techs are specified) is an Opentelemetry agent (running the Opentelemtry SDK/API) sending, via OTLP, logs metrics and traces to an Opentelemtry collector. This model can be daisy-chained.

The implementation explored here is based on the [Elastic stack](https://www.elastic.co/guide/en/observability/current/apm-open-telemetry.html), where an APM server plays the role of the collector, and sends all data into Elastic for UI interaction in Kibana's observability. Multiple agents are explored (see the [Services](#services) section).

The stack can be brought up with
```
docker compose up --build
```

Elasticsearch and Kibana are available on their usual ports; `http://localhost:9200` and `http://localhost:5601` respectively. The will accept username `elastic` and password `changeme`.

The Elastic stack has an APM server, available on `http://localhost:8200`. Using APM with Elastic requires using Fleet, which means turning on xpack security. There is a fair bit of extra red-tape involved in setting up all the usernames and passwords for the various system roles. The admin role has the password `changeme` set at start up. The rest of the roles are configured in a setup sidecar, which assigns the password `changeme` to the roles `elastic remote_monitoring_user beats_system logstash_system kibana kibana_system apm_system`. Handling passwords open, checked into code, and over http (i.e. without TLS) is NOT OK for production; only here for test purposes. The password is liberally written, unecrypted, in various areas; to see all the places grep for `changeme`.

The APM integration will create a data view called 'APM', which can be used directly in discover, or in any dashboarding. This data view gives a view on all of the traces, metrics and logs uploaded from the APM server.

### Observability

This is a main section, accessed in Kibana. From the hamburger icon on the top left, one can click on Observability.

#### Services

In Kibana, from the hamburger icon on the top left, one can click on Observability > APM > Services. This will show the services currently being monitored, which are
- a FastAPI app (traces and logs). The pipeline of traces and logs looks like fastapiapp > apmserver > elastic. Logs are available under the tab for the service, traces are available under Observability > APM > Traces.
- a fluent-bit instance pulling logs and metrics from the host system. The pipeline of host system logs and metrics looks like host > fluentbit > apmserver > elastic
    - The logs will be under a proper service name, and can be accessed under the logs tab for that service.
    - The metrics will be under a service name of 'unknown', since I haven't found a way of attaching a `service.name` to opentelemetry formatted metrics. The metrics are accessed under Observability > Infrastructure > Metrics Explorer.

#### Alerts

With metrics and logs going into Elastic's APM via Opentelemetry, one can configure alerts in Elastic. From the main hamburger icon in the top left of Kibana, one can use the left hand menu to go to Observability > Alerts. One can then create a Rule (from 'Manage Rules', probably a 'custom threshold' rule) which can then be used for monitoring and issuing alerts.