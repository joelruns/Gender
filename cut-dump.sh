#!/bin/bash/

cat ./* | egrep -n "</a>"|cut -d \= -f 2 | cut -d \> -f 1 | cut -d \" -f 2 > "$1.out";
cat "$1.out";
