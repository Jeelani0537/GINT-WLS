#!/bin/bash

#export LD_LIBRARY_PATH="/usr/lib/oracle/12.1/client64/lib"
#export ORACLE_HOME="/usr/lib/oracle/12.1/client64"

export LD_LIBRARY_PATH="/u01/app/oracle/product/12.2.0/client_1/lib"
export ORACLE_HOME="/u01/app/oracle/product/12.2.0/client_1"

echo "Current directory: " $(pwd)
cd $4
echo "Current directory: " $(pwd)

#python MHS_PM_activity_OPT.py -s $1 -a $2 -e $3 -u $5
python $5 -s $1 -a $2 -e $3 -u $6
