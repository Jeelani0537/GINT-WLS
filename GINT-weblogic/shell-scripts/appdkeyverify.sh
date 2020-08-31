#!/bin/bash

old_key=$1
new_key=$2

env=$(hostname)

paths="/opt/appdynamics/appagent/ver*/conf/controller-info.xml /opt/appdynamics/machineagent/conf/controller-info.xml /opt/appdynamics/machineagent/monitors/analytics-agent/conf/analytics-agent.properties"

for path in $paths
do
  if [ "$path" == "/opt/appdynamics/machineagent/monitors/analytics-agent/conf/analytics-agent.properties" ]
  then
    currentKey=$(grep "http.event.accessKey=" $path | sed -e 's/http.event.accessKey=//')
  else
    currentKey=$(grep "account-access-key" $path | sed -e 's/<account-access-key>//' -e 's/<\/account-access-key>//' | tr -d "[:blank:]")
  fi

  if [ "$currentKey" == "$new_key" ]
  then
    echo "$env: New appd license key: $new_key found in $path"
  else
    echo "$env: Old appd license key: $old_key found in $path"
  fi
done

