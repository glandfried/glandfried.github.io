#!/bin/bash

if [ $# \> 0 ]
then
    sed -n "/$1/,/^}/p" biblio.bib | grep url | grep -o '{.*}' | sed  's/{/"/g' | sed 's/}/"/g' | xargs wget -U --adjust-extension -O download/$1
else
    items=$(cat biblio.bib | grep @ | awk -F '{' '{print $2}' | awk -F ',' '{print $1}')
    for i in $items
    do
        if [ ! -f "download/$i" ]
	then
	    sed -n "/$i/,/^}/p" biblio.bib | grep url | grep -o '{.*}' | sed  's/{/"/g' | sed 's/}/"/g' | xargs wget -U --adjust-extension -O download/$i
        fi
    done
    echo "All biblio download"
fi



