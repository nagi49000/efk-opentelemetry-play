# efk-opentelemtry-play
A play area for an EFK stack running locally using opentelemetry for sending logs, metrics and traces.

This example uses metricbeat for sending metrics to Elastic.

The stack can be brought up with
```
docker compose up --build
```

Elasticsearch and Kibana are available on their usual ports; `http://localhost:9200` and `http://localhost:5601` respectively. The will accept username `elastic` and password `changeme`.
