#!/bin/bash

Orange='\33[0;33m'
RED='\033[0;31m'
NC='\033[0m'


set -o errexit
set -o nounset
set -o pipefail

THRESHOLD_IN_DAYS="60"
KEYSTORE=""
PASSWORD=""


usage() {
    echo "Usage: $0 --keystore <keystore> [--password <password>] [--threshold <number of days until expiry>]"
    exit
}

start() {

  ############################################
  ###### Display the validity of certs #######
  ############################################
  CURRENT=`date +%s`
  THRESHOLD=$(($CURRENT + ($THRESHOLD_IN_DAYS*24*60*60)))
  if [ $THRESHOLD -le $CURRENT ]; then
    echo "[ERROR] Invalid date."
    exit 1
  fi
  echo "Looking for certificates inside the keystore $(basename $KEYSTORE) expiring in $THRESHOLD_IN_DAYS day(s)..."
  keytool -list -v -keystore $KEYSTORE $PASSWORD 2>&1 > /dev/null
  if [ $? -gt 0 ]; then echo "Error opening the keystore."; exit 1; fi
  keytool -list -v -keystore "$KEYSTORE"  $PASSWORD | grep Alias | awk -F',' '{print $1}' | sed 's/Alias name: //' | while read ALIAS
  do
    # Iterate through all the certificate alias
    UNTIL=`keytool -list -v -keystore "$KEYSTORE" $PASSWORD -alias "$ALIAS" | grep Valid | perl -ne 'if(/until: (.*?)\n/) { print "$1\n"; }'`
    UNTIL_SECONDS=`date -d "$UNTIL" +%s`
    REMAINING_DAYS=$(( ($UNTIL_SECONDS -  $(date +%s)) / 60 / 60 / 24 ))
    if [ $THRESHOLD -le $UNTIL_SECONDS ]; then
      echo "[OK] Certificate '$ALIAS' expires in '$UNTIL' ($REMAINING_DAYS day(s) remaining)."
    elif [ $REMAINING_DAYS -le 0 ]; then
      echo "[CRITICAL] Certificate $ALIAS has already expired."
    elif [ $REMAINING_DAYS -le 30 ]; then
      echo "[WARNING] Certificate '$ALIAS' expires in '$UNTIL' ($REMAINING_DAYS day(s) remaining)."
      else
      echo "Ignore Alert"
    fi
  done
  echo "Finished execution"

}
#Validity=date
#let DIFF=(validity-REMAINING_DAYS)/86400
#echo $DIFF

while [ $# -gt 0 ]
do
  case "$1" in
    --password)
    if [ -n "$2" ]; then PASSWORD=" -storepass $2"; else echo "Invalid password"; exit 1; fi
    shift 2;;
    --keystore)
    if [ ! -f "$2" ]; then echo "Keystore not found: $1"; exit 1; else echo "Second Argument is $2"; KEYSTORE=$2; fi
    shift 2;;
    --threshold)
    if [[ $2 =~ ^[0-9]+$ ]]; then THRESHOLD_IN_DAYS=$2; else echo "Invalid threshold"; exit 1; fi
    ;;
    *)
    echo "Invalid Paramaeter"
    exit -1;
  esac
done

if [ -n "$KEYSTORE" ]
then
  start
else
  usage
fi