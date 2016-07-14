Title: Using pg_service.conf with Luigi
Date: 2016-07-14 17:42:15 +0000
lat: 41.8892138776688
long: -87.6328944003586

I was thinking about the pg_service.conf post I wrote yesterday, and wondering how to follow that practice in [Luigi](http://luigi.readthedocs.io/). It's a little tricky, because [`luigi.postgres`](http://luigi.readthedocs.io/en/stable/api/luigi.postgres.html) implements instances of `luigi.contrib.rdbms` abstract classes, and therefore expects all the abstract properties (i.e., host, database, etc.) to be specified. So, when I tried simply overriding the `connect()` method of `PostgresTarget` I was getting TypeErrors because those abstract methods weren't implemented.

I didn't want to build this up from a generic Luigi `Task`, because `luigi.postgres` and `luigi.contrib.rdbms` have a lot of really useful stuff already implemented that I would have had to repeat for myself. In the end, I found that I could just set the `rdms` properties to `None` defaults and then ignore them, while overriding `PostgresTarget.connect()` the way I wanted to. The resulting template tasks, along with a couple of simple examples of subclassing them for specific jobs are in [this Gist](https://gist.github.com/yagermadden/d515f0b1dde2c4cdd6c192e08bb33e00) which is also shown below:

```
#!python
import luigi
import luigi.postgres
import psycopg2

testdata = ([99, 'My fake plants died because I did not pretend to water'
             ' them.'],
            [100, 'I always arrive late at the office, '
            'but I make up for it by leaving early.'],
            [101, u'∩ ∪'])


class PgServiceTarget(luigi.postgres.PostgresTarget):
    """
    Target for a resource in PostgreSQL, overriding the standard PostgresTarget
    to use a pg_service.conf service name to make the connection instead of
    separate connection params
    """
    def __init__(self, service, update_id, table):
        """
        Args:
            service (str): the name of a service defined in local
                pg_service.conf file
            update_id (str): An identifier for this data set
        """
        self.service = service
        self.update_id = update_id
        self.table = table

    def connect(self):
        """
        Get a psycopg2 connection object to the database where the table is.
        """
        connection = psycopg2.connect(
            service=self.service)
        connection.set_client_encoding('utf-8')
        return connection


class PgServiceQuery(luigi.postgres.PostgresQuery):
    """
    Template task for querying a PostgreSQL database, with standard output
    method overridden to return a PgServiceTarget
    """
    # Handle the properties expected by abstract class rdbms.Query
    host = None
    database = None
    user = None
    password = None

    def output(self):
        return PgServiceTarget(service=self.service, table=self.table, update_id=self.update_id)


class PgCopyToTable(luigi.postgres.CopyToTable):
    """
    Template task for inserting a data set into Postgres via PgServiceTarget
    """
    # Handle the properties expected by abstract class rdbms.Query
    host = None
    database = None
    user = None
    password = None

    def output(self):
        return PgServiceTarget(service=self.service, table=self.table, update_id=self.update_id)


class PgExampleQuery(PgServiceQuery):
    service = luigi.Parameter(default='local')
    table = 'whoa'
    query = 'create table whoa (trival_id serial, whoa_txt text)'


class PgExampleLoad(PgCopyToTable):
    service = luigi.Parameter(default='local')
    table = 'whoa'
    columns = [("trival_id", "INT"),
               ("description", "TEXT")]

    def rows(self):
        for record in testdata:
            yield record
```
