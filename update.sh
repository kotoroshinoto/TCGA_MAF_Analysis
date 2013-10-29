#!/bin/bash
git fetch --all
git reset --hard origin/master
function EXPERM(){
	DIR=$1;
	shift;
	for EXT in "$@"
	do 
	find ./$DIR -type f -path *.$EXT -exec chmod -f +x {} \;
	done	
}
function EXPERMALL(){
	DIR=$1;
	shift;
	find ./$DIR -type f -exec chmod -f +x {} \;	
}
EXPERM cgi-bin pl pm