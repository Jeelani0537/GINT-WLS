#Ensure to source boot.properties from AdminServer/security before running this script.Run script in below format
#wlst.sh healthCheck.py enpasswd domainName fmwVersion adminHost adminPort

import sys
import commons
import wlstModule as wlm

host = sys.argv[1]
port = sys.argv[2]

def pauseJMSServers():
  wlm.serverRuntime()
  serverName = wlm.cmo.getName()
  serverStatus = wlm.cmo.getState()
  if serverStatus == "FAILED" :
    print "Server has failed already. Cannot pause JMS servers!!!"
  else:
    wlm.cd('/JMSRuntime/' + serverName + '.jms')
    print"Pausing JMS Servers"
    jmsServers = wlm.cmo.getJMSServers()
    for jmsServer in jmsServers:
      jmsServerName = jmsServer.getName()
      wlm.cd('/JMSRuntime/' + serverName + '.jms/JMSServers/' + jmsServerName)
      wlm.cmo.pauseConsumption()
      print "Consumption status for " + jmsServerName + ": " + wlm.cmo.getConsumptionPausedState()
  print "\n\n"

def shutdownServer():
  print "Shutting down server"
  wlm.shutdown(entityType='Server', ignoreSessions='false', timeOut=600, force='false', block='false')

user,passwd = commons.readCredentials()
commons.adminConnect(user, passwd, host, port)

try:
  pauseJMSServers()
except:
  errorMessage = "Error while pausing JMS Servers"
  commons.exitWithError(errorMessage)

try:
  shutdownServer()
except:
  errorMessage = "Error while running shutting down the server"
  commons.exitWithError(errorMessage)

commons.disconnectWithSuccess()
commons.exitWithSuccess()
