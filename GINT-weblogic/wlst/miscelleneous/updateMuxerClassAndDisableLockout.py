#Ensure to source boot.properties from AdminServer/security before running this script.Run script in below format
#wlst.sh healthCheck.py enpasswd domainName fmwVersion adminHost adminPort
#Description: This will disable user lockout and update muxer class to weblogic.socket.PosixSocketMuxer from weblogic.socket.NIOSocketMuxer

import sys
import commons
import wlstModule as wlm

adminHost = sys.argv[1]
adminPort = sys.argv[2]

def updateMuxerClassAndDisableLockout():
  servers = wlm.cmo.getServers()
  domainName = wlm.cmo.getName()
  wlm.cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm/UserLockoutManager/UserLockoutManager')
  wlm.cmo.setLockoutEnabled(false)
  print "\n"
  print "Disabled user lockout"
  print "\n"
  
  for server in servers :
    serverName = server.getName()
    print "In " + serverName + " tree..."
    wlm.cd('/Servers/' + serverName)
    wlm.cmo.setMuxerClass('weblogic.socket.PosixSocketMuxer')
    print "MuxerClass has been set to: weblogic.socket.PosixSocketMuxer"
    print "\n"
	
user,passwd = commons.readCredentials()
commons.adminConnect(user, passwd, adminHost, adminPort)

commons.takeSession()
  
try:
  updateMuxerClassAndDisableLockout()
except:
  errorMessage = "Error while enabling GracefulShutdownTimeout"
  commons.exitWithError(errorMessage)
 
commons.activateChanges()
commons.disconnectWithSuccess()
commons.exitWithSuccess()
