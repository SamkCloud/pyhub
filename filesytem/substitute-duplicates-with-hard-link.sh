#!/bin/sh

#fdupes -r -1 . | while read line; do j="0"; for file in ${line[*]}; do if [ "$j" == "0" ]; then j="1"; else echo "ln -f -s ${line// .*/} $file"; ln -f ${line// .*/} $file ; fi; done; done


fdupes -r -1 . | while read line
do 
	j="0"
	for file in ${line[*]}
		do 
		if [ "$j" == "0" ]
			then j="1"
		else 
			echo "ln -f ${line// .*/} $file"
			ln -f ${line// .*/} $file 
		fi
	done
done

