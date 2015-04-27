#!/bin/bash

FILE=strings.out;
k=1;
echo '###########'

cat $FILE | while read line; do
	str="https://www.okcupid.com/profile/"$line"/personality"
	touch $k
	GET $str > $k
	((k++))
done
