Title: Postgres Monitoring
Date: 2016-10-11 18:04:22 +0000
lat: 42.0717804175097
long: -87.7154614593466

## What we have in palace

#### Monitors

Via [Stackdriver](https://app.google.stackdriver.com/services/postgresql):

- Connections (count): Number of connections to PostgreSQL.
- Disk Usage (byte): Number of bytes currently being used on disk.
- Commits (count/s): Number of commits per second.
- Rollbacks (count/s): Number of rollbacks per second.
- Heap Blocks Read Rate (count/s): Number of blocks read from the heap.
- Heap Cache Hit Rate (count/s): Number of blocks read directly out of the cache.
- Index Blocks Read Rate (count/s): Number of blocks read from the index.
- Index Cache Hit Rate (count/s): Number of index blocks read directly out of the cache.
- Toast Blocks Read Rate (count/s): Number of reads from the toast blocks.
- Toast Cache Hit Rate (count/s): Number of toast blocks read directly out of the cache.
- Toast Index Blocks Read Rate (count/s): Number of blocks read from the toast index.
- Toast Index Cache Hit Rate (count/s): Number of toast index blocks read directly out of the cache.
- Operations [delete, insert, update, heap only update] (count/s): Number of rows [deleted, inserted, updated, heap only updated] in the db.
- Dead Tuples (count): Number of tuples that are dead in the db.
- Live Tuples (count): Number of tuples that are live in the db.

Plus CPU, RAM, disk, and network traffic stats on the host

All of the above are simply being passively monitored; we don't have any threshold-based alerting on any metrics.

#### Alerting policies

- Uptime Check Health on mart.pgdata.xyz fails
- Uptime Check Health on warehouse.pgdata.xyz fails
- CPU Usage is absent for greater than 5 minutes from warehouse.pgdata.xyz
- CPU Usage is absent for greater than 10 minutes from api-postgres
- CPU Usage is absent for greater than 5 minutes from mart-postgres

When raised, these all send notice to the #data channel in Slack, and push notification to TYM via the Google Could Console app.

## What we should still add

#### Things to monitor
- Count of database locks
- Duration of queries (avg, longest-running)
- Count and duration of idle-in-transaction connections
- Last checkpoint
- Actual uptime based on database connection (existing checks use ping or CPU metric availability)


#### Things to alert on
- blocking locks (at all)
- exclusive locks (threshold-based)
- connections waiting for a lock (threshold-based)
- long-running queries


#### Some options (needs research)
- Custom metrics via Stackdriver API
- [pgantenna](https://no0p.github.io/pgantenna/)
- [OPM](http://opm.io/) (Don't miss [Dockerized](https://github.com/yuhuman/OPM-Docker) version)
- Roll our own check_postgres, Nagios, collectd, graphite server
