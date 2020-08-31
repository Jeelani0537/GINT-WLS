#!/bin/bash

old_key=$1
new_key=$2
version=$3

stopagent="/usr/tmp/stopmachineagent.pid"
startagent="/usr/tmp/startmachineagent.pid"
output=pwd
echo "########################### GINT-Weblogic ############################"
echo "Starting replacing the licence key in App Dynamic App and Machine Agents"
cd /opt/appdynamics/appagent/ver$version/conf
echo "Present working directory: $(pwd)"
cp -p controller-info.xml controller-info.xml-`date +%Y%m%d-%H:%M`
echo "Backup of controller-info.xml taken"
#sed -i 's/6cvs4iglty4t/5b27fe7d-7e9f-4b65-bf5d-111e74ec951c/g' controller-info.xml
sed -i "s/$old_key/$new_key/g" controller-info.xml
#diff controller-info.xml controller-info.xml-`date +%Y%m%d-%H:%M`
sleep 5
echo "Changes done on /opt/appdynamics/appagent/ver$version/conf/controller-info.xml file"

cd /opt/appdynamics/machineagent/conf
echo "Present working directory: $(pwd)"
cp -p controller-info.xml controller-info.xml-`date +%Y%m%d-%H:%M`
echo "Backup of controller-info.xml taken"
#sed -i 's/6cvs4iglty4t/5b27fe7d-7e9f-4b65-bf5d-111e74ec951c/g' controller-info.xml
sed -i "s/$old_key/$new_key/g" controller-info.xml
#diff controller-info.xml controller-info.xml-`date +%Y%m%d-%H:%M`
sleep 5
echo "Changes done on /opt/appdynamics/machineagent/conf/controller-info.xml file"


cd /opt/appdynamics/machineagent/monitors/analytics-agent/conf
cp -p analytics-agent.properties analytics-agent.properties-`date +%Y%m%d-%H:%M`
echo "Backup of analytics-agent.properties  taken"
#sed -i 's/6cvs4iglty4t/5b27fe7d-7e9f-4b65-bf5d-111e74ec951c/g' analytics-agent.properties
sed -i "s/$old_key/$new_key/g" analytics-agent.properties
#diff analytics-agent.properties analytics-agent.properties-`date +%Y%m%d-%H:%M`
sleep 5
echo "Changes done on /opt/appdynamics/machineagent/monitors/analytics-agent/conf/analytics-agent.properties file"

echo "Restart the Machine Agent to reflect the changes"
echo "############### Stop Machine Agent ################"
ps -fu oracle | grep /opt/appdynamics/machineagent | grep -v grep | awk '{print $2}' > /usr/tmp/stopmachineagent.pid

echo "Process id of existing Machine Agent: $(cat /usr/tmp/stopmachineagent.pid)"
kill -15 $(cat /usr/tmp/stopmachineagent.pid)
sleep 15
echo "Check the process of Machine Agent has killed"

if [ ! -n "$stopagent" ]
then
      echo "Process is not stopped"
      kill -15 $(cat /usr/tmp/stopmachineagent.pid)
else
      echo "Process is Killed"
fi
sleep 10
echo "############ Start the Machine Agent #############"

/opt/appdynamics/machineagent/bin/machine-agent -d -p /opt/appdynamics/machineagent/pidfile -j /opt/appdynamics/machineagent/jre
sleep 5
echo "Check Machine Agent status"
ps -fu oracle | grep /opt/appdynamics/machineagent | grep -v grep | awk '{print $2}' > /usr/tmp/startmachineagent.pid

if [ -z "$startagent" ]
then
      echo "Machine Agent not started"
      #ps -fu oracle | grep /opt/appdynamics/machineagent  | grep -v grep | awk '{print $2}' > /usr/tmp/startmachineagent.pid
      /opt/appdynamics/machineagent/bin/machine-agent -d -p /opt/appdynamics/machineagent/pidfile -j /opt/appdynamics/machineagent/jre
else
      echo "Machine Agent is started"
fi
echo "Process id of Machine Agent After restart: $(cat /usr/tmp/startmachineagent.pid)"
rm /usr/tmp/stopmachineagent.pid
rm /usr/tmp/startmachineagent.pid

echo Done!
echo "############################ Changes Completed ########################"

