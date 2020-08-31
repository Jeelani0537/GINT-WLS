#############################################################################################
#Prepared by: Praveen Raj Kumar Kandregula
#Purpose: This script is meant to shutdown&untaget/start the datasources
#############################################################################################

import sys
import commons
import wlstModule as wlm
host = sys.argv[1]
port = sys.argv[2]
dataSources = sys.argv[3]
ds_activity = sys.argv[4]

def shutdownDS(dataSources):
  servers = wlm.cmo.getServers()
  wlm.domainRuntime()
  for server in servers:
    serverName = server.getName()
    print '**************************************************************************'
    print '==>In ' + serverName + ' tree...'
    for dsName in dataSources.split(','):
      if wlm.getMBean('/ServerRuntimes/' + serverName + '/JDBCServiceRuntime/' + serverName + '/JDBCDataSourceRuntimeMBeans/' + dsName):
        print '====>Shutting down ' + dsName + ' on ' + serverName
        wlm.cd('/ServerRuntimes/' + serverName + '/JDBCServiceRuntime/' + serverName + '/JDBCDataSourceRuntimeMBeans/' + dsName)
        objectArray = jarray.array([], java.lang.Object)
        stringArray = jarray.array([], java.lang.String)
        invoke('shutdown', objectArray, stringArray)
        print '====>Successfully shutdown ' + dsName + ' on ' + serverName
      else:
        print serverName + ' is not in the targets of ' + dsName
      print '\n'
  print '**************************************************************************\n'
  
def getClusterName():
  wlm.serverConfig()
  clusters = wlm.cmo.getClusters()
  if len(clusters) == 1:
    for cluster in clusters:
      clusterName = cluster.getName()
      return clusterName
  else:
    errorMessage = "More than one cluster found"
    commons.exitWithError(errorMessage)

def unTargetDS(dataSources):
  print '**************************************************************************'
  for dsName in dataSources.split(','):
    if wlm.getMBean('/JDBCSystemResources/' + dsName):
      print '==>Removing targets from ' + dsName
      wlm.cd('/JDBCSystemResources/' + dsName)
      wlm.set('Targets',jarray.array([], ObjectName))
      print '==>Targets have been removed from ' + dsName + '\n'
  print '**************************************************************************\n'
  
def targetDS(clusterName,dataSources):
  print '**************************************************************************'
  for dsName in dataSources.split(','):
    if wlm.getMBean('/JDBCSystemResources/' + dsName):
      print '==>Assiging targets to ' + dsName
      wlm.cd('/JDBCSystemResources/' + dsName)
      wlm.set('Targets',jarray.array([ObjectName('com.bea:Name=' + clusterName + ',Type=Cluster')], ObjectName))
      print '==>Targets for ' + dsName + ' have been updated to ' + clusterName
    else:
      print dsName + ' is not found'
  print '**************************************************************************\n'

user,passwd = commons.readCredentials()
commons.adminConnect(user, passwd, host, port)

if ds_activity == 'stop':
  shutdownDS(dataSources)
  commons.takeSession()
  unTargetDS(dataSources)
  commons.activateChanges()
elif ds_activity == 'start':
  clusterName = getClusterName()
  commons.takeSession()
  targetDS(clusterName,dataSources)
  commons.activateChanges()
  
commons.disconnectWithSuccess()
commons.exitWithSuccess()
