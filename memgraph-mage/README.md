# Memgraph stack

The stack includes `memgraph-mage`, which is the actual processing enginer, and `memgraph-lab`, which is a UI, available on `http://localhost:3000`.

On connecting to the UI, one can connect to `memgraph-mage`, click on `Query execution`, and `Cypher editor` to make CYPHER queries, and in particular use memgraph's elasticsearch serialization plugin (the Dockerfile includes some code mods on the serialization plugin).

One can check connection ability to the elasticsearch instance, in the `Cypher editor`, with
```
CALL elastic_search_serialization.connect("http://elasticsearch:9200")
YIELD connection_status
RETURN connection_status;
```
and running the query. If connection works, then retreiving results should also work, which the serialization plugin also supports, e.g. on an index called `fluent-bit-metrics-disk`
```
CALL elastic_search_serialization.search("fluent-bit-metrics-disk",  "{\"match_all\": {}}", 1000, 0)
YIELD result
RETURN result;
```

### Creating graphs from elastic output (for analysis)

One can get the last minute of activity with
```
CALL elastic_search_serialization.search("fluent-bit-metrics-cpu",  
'{"range": {"@timestamp": {"time_zone": "+00:00", "gte": "now-1m", "lte": "now"}}}',
1000, 0)
YIELD result
RETURN result.hits.hits;
```
One can build up a graph (where the each timestamp becomes a pizza node for log messages and metrics activity) with
```
CALL elastic_search_serialization.search("fluent-bit-metrics-cpu",  
'{"range": {"@timestamp": {"time_zone": "+00:00", "gte": "now-1m", "lte": "now"}}}',
1000, 0)
YIELD result
UNWIND result.hits.hits AS h
MERGE (t:Timepoint {stamp: datetime(left(h._source.`@timestamp`, 19) + "Z")})
MERGE (m:MetricCpu {cpu: h._source.cpu_p})
MERGE (t)-[:HAS_CPU_VALUE]->(m);

CALL elastic_search_serialization.search("fluent-bit-metrics-memory",  
'{"range": {"@timestamp": {"time_zone": "+00:00", "gte": "now-1m", "lte": "now"}}}',
1000, 0)
YIELD result
UNWIND result.hits.hits AS h
MERGE (t:Timepoint {stamp: datetime(left(h._source.`@timestamp`, 19) + "Z")})
MERGE (m:MetricMem {mem_used: h._source.`Mem.used`})
MERGE (t)-[:HAS_MEM_USED]->(m);

CALL elastic_search_serialization.search("fluent-bit-metrics-disk",  
'{"range": {"@timestamp": {"time_zone": "+00:00", "gte": "now-1m", "lte": "now"}}}',
1000, 0)
YIELD result
UNWIND result.hits.hits AS h
MERGE (t:Timepoint {stamp: datetime(left(h._source.`@timestamp`, 19) + "Z")})
MERGE (m:MetricDisk {mem_used: h._source.bytes_free})
MERGE (t)-[:HAS_DISK_BYTES_FREE]->(m);

CALL elastic_search_serialization.search("fluent-bit-metrics-diskio",  
'{"range": {"@timestamp": {"time_zone": "+00:00", "gte": "now-1m", "lte": "now"}}}',
1000, 0)
YIELD result
UNWIND result.hits.hits AS h
MERGE (t:Timepoint {stamp: datetime(left(h._source.`@timestamp`, 19) + "Z")})
MERGE (m:MetricDiskio {read_size: h._source.read_size, write_size: h._source.write_size})
MERGE (t)-[:HAS_DISKIO]->(m);

CALL elastic_search_serialization.search("fluent-bit-logging",  
'{"range": {"@timestamp": {"time_zone": "+00:00", "gte": "now-1m", "lte": "now"}}}',
1000, 0)
YIELD result
UNWIND result.hits.hits AS h
MERGE (t:Timepoint {stamp: datetime(left(h._source.`@timestamp`, 19) + "Z")})
MERGE (m:LogMessage {log: h._source.log})
MERGE (t)-[:HAS_LOG_MESSAGE]->(m);
```
### Running graph analytics

One can then explore the graph to, say, find the 'busiest' Timepoint nodes (by degree centrality)
```
CALL degree_centrality.get("out")
YIELD degree, node
RETURN degree, node ORDER BY degree DESC LIMIT 10
```
