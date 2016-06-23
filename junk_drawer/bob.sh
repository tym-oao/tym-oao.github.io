#!/bin/bash

title=$1
filen=$(echo "$title" | perl -ne 'print lc')
filet=${filen//' '/'-'}'.md'
echo "$filet"
