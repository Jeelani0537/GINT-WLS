##################################################################################################################
#######################################Use below format to call the script########################################
#####<wlst.sh with full path> serverStatus.py <console-username> <console-password> <admin-host> <admin-port>#####
##################################################################################################################

import sys

def printException():
  print "Invalid usage of this script is identified. \nRun this script in below format"
  print "<wlst.sh with full path> serverStatus.py <console-username> <console-password> <admin-host> <admin-port>"

#Command line args validation
if len(sys.argv) != 5:
  printException()
else:
  try:
    user = sys.argv[1]
    passwd = sys.argv[2]
    adminHost = sys.argv[3]
    adminPort = sys.argv[4]

    connect(user, passwd, 't3://' + adminHost + ':' + adminPort)
    serversList = cmo.getServers()
    domainRuntime()

    for server in serversList:
      sname = server.getName()
      cd('/ServerRuntimes/' + str(sname))
      overallHealth = str(cmo.getOverallHealthState())
      for item in overallHealth.split(","):
        if 'State' in item:
          state, health = item.split(":")
          print sname + "  " + health
    disconnect()
  except:
    printException()
exit()