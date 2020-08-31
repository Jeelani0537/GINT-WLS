#!/bin/bash

stopagent="/usr/tmp/stopmachineagent.pid"
startagent="/usr/tmp/startmachineagent.pid"
output=pwd

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
echo "############################ Restart Completed ########################"

