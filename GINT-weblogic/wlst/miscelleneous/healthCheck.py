#############################################################################################
#Prepared by: Praveen Raj Kumar Kandregula
#Purpose: This checks health of a domain through WLST.
#############################################################################################

import sys
import commons
import wlstModule as wlm

host = sys.argv[1]
port = sys.argv[2]
outputFile = "/tmp/health-check-output.out"

def serversStatus():
  serversList = wlm.cmo.getServers()
  wlm.domainRuntime()

  try:
    for server in serversList:
      sname = server.getName()
      wlm.cd('/ServerRuntimes/' + str(sname))
      overallHealth = str(wlm.cmo.getOverallHealthState())
      for item in overallHealth.split(","):
        if 'State' in item:
          state, health = item.split(":")
          print sname + "  " + health
  except:
    errorMessage = "An error occured while checking servers status"
    commons.exitWithError(errorMessage)

user,passwd = commons.readCredentials()
commons.adminConnect(user, passwd, host, port)

domainName = wlm.cmo.getName()

old_stdout = sys.stdout
sys.stdout = open(outputFile, 'a+')

serversStatus()

sys.stdout = old_stdout

commons.disconnectWithSuccess()
commons.exitWithSuccess()
