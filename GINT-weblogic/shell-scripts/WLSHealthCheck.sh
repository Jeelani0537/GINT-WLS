#!/bin/bash
RED='\033[0;31m'
NC='\033[0m'
GRN='\033[0;32m'
YLW='\033[1;33m'
NOW=$(date +%b-%d-%Y-%H%M%S)
ALOG=$(echo "HC-$NOW.log")
LOG=$(echo "WLS_HC-$NOW.log")
env=$(hostname -a | head -c2)
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" | tee  $LOG
echo "+++++++++++++++++++++++ WLS Basic Health Checks ++++++++++++++++++++++++" | tee -a $LOG
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" | tee -a $LOG
echo " " | tee -a $LOG
#checking the last reboot time
echo "Checking the Last reboot time"  | tee -a $LOG
echo "============================="  | tee -a $LOG
datenow=$(date '+%Y-%m-%d %H:%M')
lastboot=$(who -b | awk '{print $3,$4}')
uphours=$(echo $(( ($(date --date="$datenow" +%s) - $(date --date="$lastboot"  +%s) )/(60*60) )))
if [[ $uphours  -gt 24 ]];
then
echo -e "${GRN}No server reboot in last 24 hours.${NC}"  | tee -a $LOG
bootmsg=$(echo "No server reboot in last 24 hours")
bootstat=$(echo -e ${GRN}"  FINE" ${NC})
else
echo -e "${RED}Server reboot happend before $uphours hrs. ${NC}"  | tee -a $LOG
bootmsg=$(echo "${RED}Server reboot happend ")
bootstat=$(echo -e ${RED}" DEVIATION" ${NC})
fi

echo -e "The server was last rebooted on ${YLW}$lastboot${NC}"  | tee -a $LOG
echo ""  | tee -a $LOG

#Checking vip status
echo "VIP Status"  | tee -a $LOG
echo "========== "  | tee -a $LOG
echo ""  | tee -a $LOG
if [[ $env = "it" ]] || [[ $env = "pp" ]];
then
vipstatus=$(sudo wlipctl status ip -a | grep -i inactive)
echo "Current Status :"  | tee -a $LOG
sudo wlipctl status ip -a  | tee -a $LOG
echo ""  | tee -a $LOG
  if [[ $($vipstatus | wc -l) -gt 0 ]];
  then
    echo -e "${RED}VIPs are down, Please check the below VIPS and start.${NC} \n $vipstatus"  | tee -a $LOG
    echo $vipstatus  | tee -a $LOG
    vipresult=$(echo "VIPs are down")
    vipstat=$(echo -e ${RED}" DOWN" ${NC})
  else
    echo -e "${GRN}VIPs are up and running fine.${NC}"  | tee -a $LOG
    vipresult=$(echo "VIPs are fine")
    vipstat=$(echo -e ${GRN}" RUNNING" ${NC})
  fi
else
  echo "VIP is not applicable here as this is lower environments."  | tee -a $LOG
  vipstat=$(echo -e ${YLW}"   N/A  " ${NC})
  vipresult=$(echo "VIPs not applicable as this is lower environments.")
fi
echo " "  | tee -a $LOG

#Checking File systems
echo "Filesystem Status"  | tee -a $LOG
echo "================="  | tee -a $LOG
echo " "  | tee -a $LOG
df -h  | tee -a $LOG
echo " "  | tee -a $LOG
if [[ -f ./FSstatus/FSstatus ]];
then
df -h | awk '{print $6}' >> ./FSstatus/FSstatus-$NOW
fsstatus=$(diff -y --suppress-common-lines ./FSstatus/FSstatus ./FSstatus/FSstatus-$NOW | wc -l)

  if [[ $fsstatus -gt 0 ]];
  then
  echo -e ${RED}"There are issues in the File system, please check below File systems with GLinux."${NC}  | tee -a $LOG
  echo ""  | tee -a $LOG
  diff -y --suppress-common-lines ./FSstatus/FSstatus ./FSstatus/FSstatus-$NOW  | tee -a $LOG
  fsresult=$(echo "Issues in File system, please check.")
  fsstat=$(echo -e ${RED}"DEVIATION" ${NC})
  else
  echo -e ${GRN}"File system Looks good"${NC}  | tee -a $LOG
  fsresult=$(echo "File system Looks fine")
  fsstat=$(echo -e ${GRN}" FINE" ${NC})
  fi
else
echo -e ${RED}"Issues in comparing status, please check the FS status manually."${NC} | tee -a $LOG
fsstat=$(echo -e ${RED}"  ERROR " ${NC})
fsresult=$(echo "Unable to compare status, please check manually.")
fi
echo ""  | tee -a $LOG

#Checking Stale sessions
echo "Checking if there are any Stale sessions"  | tee -a $LOG
echo "========================================"  | tee -a $LOG
stale=$(df -h | grep -i stale)

if [[ $stale == "" ]];
then
echo -e ${GRN}"There are no stale sessions"${NC}  | tee -a $LOG
stalesession=$(echo "No Stale sessions")
stalestat=$(echo -e ${GRN}"  FINE" ${NC})
else
echo -e "${YLW}There are some stale NetApp snapshots Please check with GLinux"${NC}  | tee -a $LOG
echo $stale  | tee -a $LOG
stalesession=$(echo "Stale sessions found")
stalestat=$(echo -e ${RED}" DEVIATION" ${NC})
fi
echo ""  | tee -a $LOG

#Checking Splunk agent status
echo -e "Splunk Agent Status \n==================="  | tee -a $LOG
splunk=$(ps -ef | grep splunk | grep process-runner | awk '{print $NF}')
if [ "$splunk" = "[process-runner]" ]
then
echo -e "${GRN}Splunk agent is Up"${NC}  | tee -a $LOG
splunkres=$(echo  "Splunk agent is Up")
splunkstat=$(echo -e ${GRN}" RUNNING" ${NC})
else
echo "Service is Down"  | tee -a $LOG
splunkstat=$(echo -e ${RED}" DOWN" ${NC})
splunkres=$(echo "Splunk agent is down")
fi

#Checking OEM Agent status
echo -e "\nOEM Agent Status \n================= "  | tee -a $LOG
oemstatus=$(/u01/oracleagent/agent_inst/bin/emctl status agent | grep -i "Agent is Running and Ready" | wc -l)
if [[ $oemstatus == 1 ]];
then
echo -e ${GRN}"Agent is Running and Ready"${NC}  | tee -a $LOG
oemagentres=$(echo "Agent is Running")
oemstat=$(echo -e ${GRN}" RUNNING" ${NC})
else
echo -e ${YLW}"OEM Agent is not running"${NC}  | tee -a $LOG
oemagentres=$(echo "Agent not Running")
oemstat=$(echo -e ${RED}" DOWN" ${NC})
fi
echo ""  | tee -a $LOG
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"  | tee -a $LOG
echo -e "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ ${GRN} RESULT ${NC} ++++++++++++++++++++++++++++++++++++++++++++++++++++"  | tee -a $LOG
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"  | tee -a $LOG
echo -e "\t  Name    \t \t || \t \t   Status \t \t || \t \t Comments"   | tee -a $LOG
echo "+++++++++++++++++++++++++++++++++||++++++++++++++++++++++++++++++++++++++||+++++++++++++++++++++++++++++++++++++++++++++++++"  | tee -a $LOG
echo -e "${YLW} Server Last Reboot on ${NC} \t || \t \t $bootstat  \t \t || \t $bootmsg"  | tee -a $LOG
echo -e "${YLW} VIP Status  ${NC} \t \t \t || \t \t $vipstat \t \t || \t $vipresult"  | tee -a $LOG
echo -e "${YLW} File system Status ${NC} \t \t || \t \t $fsstat \t \t || \t $fsresult"  | tee -a $LOG
echo -e "${YLW} Stale sessions ${NC} \t \t ||\t \t $stalestat \t \t || \t $stalesession"  | tee -a $LOG
echo -e "${YLW} Splunk Agent  ${NC} \t \t ||\t \t $splunkstat \t \t || \t $splunkres"  | tee -a $LOG
echo -e "${YLW} OEM Agent  ${NC} \t \t \t || \t \t $oemstat \t \t || \t $oemagentres"  | tee -a $LOG
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"  | tee -a $LOG
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"  | tee -a $LOG
echo -e " The output file is availabe at ${GRN}/u01/WLSHealthCheck/$LOG${NC}"