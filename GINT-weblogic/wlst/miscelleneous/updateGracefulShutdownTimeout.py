#Ensure to source boot.properties from AdminServer/security before running this script.Run script in below format
#wlst.sh healthCheck.py enpasswd domainName fmwVersion adminHost adminPort
#Description: This will update GracefulShutdownTimeout value to 600

import sys
import commons
import wlstModule as wlm

adminHost = sys.argv[1]
adminPort = sys.argv[2]

def updateGracefulShutdownTimeout():
  servers = wlm.cmo.getServers()
  for server in servers:
    serverName = server.getName()
    print "In " + serverName + " tree"
    wlm.cd('/Servers/' + serverName)
    wlm.cmo.setGracefulShutdownTimeout(600)
    print "GracefulShutdownTimeout has been updated to 600"
    print "\n"

user,passwd = commons.readCredentials()
commons.adminConnect(user, passwd, adminHost, adminPort)

commons.takeSession()

try:
  updateGracefulShutdownTimeout()
except:
  errorMessage = "Error while enabling GracefulShutdownTimeout"
  commons.exitWithError(errorMessage)

commons.activateChanges()
commons.disconnectWithSuccess()
commons.exitWithSuccess()
