Title: pg_service + psycopg2 = ❤️
Date: 2016-07-13 16:13:30 +0000
lat: 41.8892418555794
long: -87.6326868892114

A couple of days ago I learned about the [pg_service.conf file](https://www.postgresql.org/docs/current/static/libpq-pgservice.html) in Postgres, and posted about it to my teammates in Slack. It lets you store connection parameters under single service names, using square-bracked "INI file" format. This makes connecting to frequently-used hosts and databases much easier. For example, with a `pg_service.conf` like...

```
#!ini
[mydb]
host=somehost
port=5433
user=someuser
dbname=mydatabase
```

...then you can go `PGSERVICE=mydb psql` at the command line, and Bob's your uncle. (This is extra handy if you have the `PGPASSWORD` envar set to the password for `someuser`.) Instead of always setting the PGSERVICE variable, I also export that to my most-often-used service (the warehouse instance, in my case) in my `.bashrc`. Another way I made this easier on myself is with by adding a simple alias-like function (I used a function because aliases can't take arguments):

```
#!bash
pg() { PGSERVICE=$1 psql

}
```

The other noteworthy thing here, is that the defined services work at the libpq level, which means that any native postgresql driver (for instance psycopg2 😉) can use them as well.

```
#!python3
import psycopg2

conn = psycopg2.connect(service='mydb', password='secret')  # or set PGPASSWORD
```

I made a more complete example in [this gist](https://gist.github.com/tym-oao/33baf67bb332cebc4b20f7211dbedf59). I suggest we should use this manner of provisioning database connections as a matter of policy:

- `ADD` a pg_service.conf file to your Docker image (likely better: provide for one to be mounted in at run time).
- Use Kubernetes secret to set `PGPASSWORD` in the environment
- Pass the service name to the psycopg2 (or whichever driver) connection method

It just makes sense.
