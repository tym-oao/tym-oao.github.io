Title: Stupid bash tricks No. 17: Editing on the fly
Date: 2016-12-22 15:11:04
lat: 42.071776
long: -87.715259


So, for a while now I've been keeping quick notes in text file in "bullet log" format &mdash; almost a sort of private Twitter for myself. The entry format is simple: a timestamp, the note content, and finally a section marker to set of each entry from the next. Like so:

```text
2016-08-10T13:57:46Z

I'm proud to say I've officially been riding fixed-gear bike long enough that freewheel feels weird now.

§
```

I like to make it easy on myself to add stuff to this file, so I whipped up a quick &amp; dirty little bash script to automate the timestamp and section marker around the entry, and then append the result to the end of the file. For a long time, this has treated STDIN as a heredoc:


```bash
#!/bin/bash

TPATH=~/Dropbox/bullet/b0.md  # the log file itself
# here's where it waits for input, then assigns to $CONTENT:
CONTENT=$(cat)
# wrap in timestamp and section symbol
date -u +%FT%TZ >> $TPATH
echo "" >> $TPATH
echo "$CONTENT" >> $TPATH
echo -e "\n&sect;\n" >> $TPATH
atom $TPATH
```

This was fine, but lately I was thinking I'd rather be writing the entry portion in Atom instead of just hanging there until I hit ctl-d. So, just the other day, I revised it to work like this:

```bash
#!/bin/bash
TPATH=~/Dropbox/bullet/b0.md
echo "" > /tmp/entry
atom --wait /tmp/entry
date -u +%FT%TZ >> $TPATH
echo "" >> $TPATH
cat /tmp/entry >> $TPATH
echo -e "\n&sect;\n" >> $TPATH
atom $TPATH
```

So, now where I used to get a prompt to type the entry, and Atom window opens a blank temp file instead, and then the script waits for me to save and close that before going on with the rest of its business. It's a little thing, but pretty sweet in practice.
