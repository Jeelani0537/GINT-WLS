import sys
import commons
import wlstModule as wlm

adminHost = sys.argv[1]
adminPort = sys.argv[2]

def RJVMErrorFix():
  servers = wlm.cmo.getServers()
  for server in servers:
    serverName = server.getName()
    if serverName != "AdminServer" :
      print "In " + serverName + " tree"
      wlm.cd('/Servers/' + serverName)
      wlm.cmo.setCompleteMessageTimeout(120)
      print "Changes have been implemented"
      print "\n"

user,passwd = commons.readCredentials()
commons.adminConnect(user, passwd, adminHost, adminPort)
commons.takeSession()

RJVMErrorFix()

commons.activateChanges()
commons.disconnectWithSuccess()
commons.exitWithSuccess()
