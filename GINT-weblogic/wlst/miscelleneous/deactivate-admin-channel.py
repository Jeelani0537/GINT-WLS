import sys
import commons
import wlstModule as wlm

adminHost = sys.argv[1]
adminPort = sys.argv[2]

def deactivateAdminChannel():
  wlm.cd('/Servers/AdminServer/NetworkAccessPoints/AdminChannel')
  print "\nDisabling AdminChannel..."
  wlm.cmo.setEnabled(false)
  print "\n"

user,passwd = commons.readCredentials()
commons.adminConnect(user, passwd, adminHost, adminPort)
commons.takeSession()

deactivateAdminChannel()

commons.activateChanges()
commons.disconnectWithSuccess()
commons.exitWithSuccess()
