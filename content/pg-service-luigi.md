Title: Using pg_service.conf with Luigi
Date: 2016-07-14 17:42:15 +0000
lat: 41.8892138776688
long: -87.6328944003586

I was thinking about the pg_service.conf post I wrote yesterday, and wondering how to follow that practice in [Luigi](http://luigi.readthedocs.io/). It's a little tricky, because [`luigi.postgres`](http://luigi.readthedocs.io/en/stable/api/luigi.postgres.html) implements instances of `luigi.contrib.rdbms` abstract classes, and therefore expects all the abstract properties (i.e., host, database, etc.) to be specified. So, when I tried simply overriding the `connect()` method of `PostgresTarget` I was getting TypeErrors because those abstract methods weren't implemented.

I didn't want to build this up from a generic Luigi `Task`, because `luigi.postgres` and `luigi.contrib.rdbms` have a lot of really useful stuff already implemented that I would have had to repeat for myself. In the end, I found that I could just set the `rdms` properties to `None` defaults and then ignore them, while overriding `PostgresTarget.connect()` the way I wanted to. The resulting template tasks, along with a couple of simple examples of subclassing them for specific jobs are in [this Gist](https://gist.github.com/yagermadden/d515f0b1dde2c4cdd6c192e08bb33e00) which is also shown below:

```#!python
[gist:id=d515f0b1dde2c4cdd6c192e08bb33e00]
```
