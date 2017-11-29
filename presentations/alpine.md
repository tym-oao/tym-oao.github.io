# Alpine linux as your container base image


Thomas Yager-Madden 2015-10-22
---

## Alpine

```
FROM alpine:latest
RUN apk add --update python python-dev py-pip && rm -rf /var/cache/apk/*
```
- Think of it as busybox with a decent package manager
- Originally for embedded systems, growing in popularity as a Docker base image

Note: still small installed base compared even with BusyBox
---

## Why it rocks
- 5MB! (versus `ubuntu:latest == 188MB`)
    - 1 layer
- package repos are super-current
    - but you can choose degrees of stability (main/edge/testing)
- Gaining traction in the Docker community
- \#gliderlabs is responsive on IRC and/or GitHub
- Also supported by Docker (officially on Docker 1.8.3, best-effort down to 1.6)

Note: - base image size not *that* important due to cache and copy-on-write
      but: does matter, e.g. during `push` and `pull` operations, CI builds, &c.
      also good for security (smaller footprint, fewer possible exploit vectors)
      and scale out (base image needed on all nodes)
---

## Why it sucks
- unfamiliar toolchain
    - `musl` != `glibc`, `apk` != `apt-get`, `ash` != `bash`, &c.
    - generally has what you need, but names may differ
- DNS is broken
    - musl-libc's resolv.conf doesn't have `search` or `domain`
- user base is still small compared to ubuntu/debian
- cron is weird (just inherited from busybox)
- possible performance issues (known issue with `grep`, maybe others?)

Note: - Things can misbehave in unexpected ways (see toolchain above) - Docs are good, but issues still tricky to resolve - Can make it harder to tell Alpine issues from code issues - have to install in user crontab - launch command is different (/usr/sbin/crond)

---

## Other options

- Debian instead of Ubuntu saves about 100MB
- Tutum offers `alpine-base` which adds S6 and dnsmasq
- BusyBox + opkg