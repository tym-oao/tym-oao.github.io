title: Postgres Monitoring Trial Findings
date 2016-11-08 12:07:58
lat: 41.888791
long: -87.632138

In order to supplement the [monitoring available in Stackdriver](http://devblog.ty-m.xyz/postgres-monitoring.html), I took a look at a number of options, as noted in [this card](https://trello.com/c/1pWdNWVM).

## TL;DR

I'm not overjoyed about any of the solutions I tried, although OPM could do the job if we can't come up with anything else.

## [pgantenna](https://no0p.github.io/pgantenna/)

This looked promising, based on the style of the project homepage, and the  helpful documentation. There was already a [docker image](https://hub.docker.com/r/no0p/pgantenna/) available, so getting this up and running was simple.

The app gathers data from a Postgres extension called [pgsampler](http://no0p.github.io/pgsampler/). Building this and installing it a postgres container was easy and straightforward: `make && make install` and then add to `postgresql.conf` as a shared_preload_libraries value.

Unfortunately, the pgantenna server just served a default Apache page on port 80, and I was unable to noodle out what the URL for the pgantenna app. At this point I noticed that the project hasn't had a new commit in 2 years, so it was unlikely that asking the developer for help would do much, and I abandoned the effort here.

**Verdict**: doesn't actually work.

## [OPM](http://opm.io/)

This turns out to be a vended distribution of Nagios, with a custom UI wrapper, and with config and commands for Postgres already included (although still requiring further customization), and its own [Nagios plugin](https://github.com/OPMDG/check_pgactivity) (an alternative to the more widely-used [`check_postgres`](https://bucardo.org/wiki/Check_postgres)).

#### Pros
- Can do everything Nagios does (threshold-based altering + some metric graphs) without so much of the Nagios setup. Indeed, it actually _is_ Nagios, with some of the Postgres-specific stuff taken care of already.
- Nicer looking front-end than Nagios for monitoring
- `check_pgactivity` does a lot of the more useful things in `check_postgres` without as much complexity/bloat. Certainly covers what we're looking for.

#### Cons
- It's still Nagios, therefore an ugly beast
- Feels like both more and less than what I'm looking for (i.e., too heavyweight but also not great).

**Verdict**: Could be workable, but I'm not sold

#### Next Steps
- Research/investigate Stackdriver custom metrics as a way to do this monitoring
    - Would have the advantage of integration with GCP account and the monitoring we are already using it for
- Draft more detailed plan for "rolling our own" solution
    - Unlike my earlier post, I would be interested not in setting up a Graphite server, but a CLI thing like [pg_view](https://github.com/zalando/pg_view).
    - Although, we'd still have to solve the problem of active/push altering
