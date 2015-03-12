#!/usr/bin/sh
# convert a list in a txt with hostname in a IP address

while read line; do
  
#	dig +short $line
#	host unix.stackexchange.com | awk '/has address/ { print $4 }'
#	nslookup unix.stackexchange.com | awk '/^Address: / { print $2 }'
#	dig unix.stackexchange.com | awk '/^;; ANSWER SECTION:$/ { getline ; print $5 }'
	echo $line"|"$(host $line | awk '/has address/ { print $4 }')
	
done <$1

