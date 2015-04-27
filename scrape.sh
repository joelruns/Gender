#!/bin/bash
# path
p=$(pwd)
	echo $p > .path;
# count
c=2000
# uniques
uniq=$(date +%s).$c

# match filter girls
key="https://www.okcupid.com/match?filter1=0,34&filter2=2,18,40&filter3=5,3600&filter4=25,8000,10000&filter5=1,1&locid=0&timekey=1&psort1=26,10000,100&sort1=0,70&custom_search=0&fromWhoOnline=0&mygender=m&update_prefs=1&sort_type=0&sa=1&using_saved_search=&count="$c

# curl for fetching matches
curl "$key"$c -o "out.txt";
cat out.txt | tidy | grep -n username= | cat > tmp

cp tmp $p"/.dumps/"$uniq".tidy.out";
# cutdump parses the output
cat tmp | bash cut-dump.sh meta/girl

rm tmp
mv out.txt ./.dumps/$uniq."curl.out"
# use python to create an array of profile URLS
python get-urls.py meta/girl.out meta/girl-url.out
python get-profile.py girl

# match filter boys
key="https://www.okcupid.com/match?filter1=0,20&filter2=2,18,40&filter3=5,3600&filter4=25,8000,10000&filter5=1,1&locid=0&timekey=1&psort1=26,10000,100&sort1=0,70&custom_search=0&fromWhoOnline=0&mygender=f&update_prefs=1&sort_type=0&sa=1&using_saved_search=&count="$c

# curl for fetching matches
curl "$key"$c -o "out.txt";
cat out.txt | tidy | grep -n username= | cat > tmp

cp tmp $p"/.dumps/"$uniq".tidy.out";
# cutdump parses the output
cat tmp | bash cut-dump.sh meta/boy

rm tmp
mv out.txt ./.dumps/$uniq."curl.out"
# use python to create an array of profile URLS
python get-urls.py meta/boy.out meta/boy-url.out
python get-profile.py boy

# run classifier
python classifier.py
