# efk-stack-play
A play area for an EFK stack running locally.

The fluent-bit build involves building the vdisk fluent-bit plugin, and dropping it into a fluent-bit image.

The stack can be brought up with
```
docker compose up --build
```

Elasticsearch and Kibana are available on their usual ports; `http://localhost:9200` and `http://localhost:5601` respectively.

There is also a memgraph stack that can hook up to Elasticsearch. This acts as a graph-based analytics service.
