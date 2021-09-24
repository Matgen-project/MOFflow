#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
read -p "Enter the current number of jobs:" jobnum

yhq | awk '{print $1;}' | sed -n "1,${jobnum}p" > joblist
exit 0
#python clean.sh
