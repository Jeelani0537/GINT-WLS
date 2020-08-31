####This has been prepared while performing TAS000000830091 and TAS000000830331
#Call script in below format
#<wlst.sh> <script.py> <user> <password> <adminHost> <adminPort>

import sys

user = sys.argv[1]
passwd = sys.argv[2]
adminHost = sys.argv[3]
adminPort = sys.argv[4]

try:
  connect(user, passwd, 't3://' + adminHost + ':' + adminPort)
except:
  print "Unable to connect to AdminServer"

servers = cmo.getServers()

try:
  edit()
  startEdit()
except:
  #errorMessage = "Unable to take session. See if there are ny open sessions"
  #exitWithError(errorMessage)
  print "Unable to take session. See if there are ny open sessions"

for server in servers:
  serverName = server.getName()
  if serverName != "AdminServer":
    print "Updating " + serverName
    cd('/Servers/' + serverName)

    print "Current CompleteMessageTimeout: " + str(cmo.getCompleteMessageTimeout())
    cmo.setCompleteMessageTimeout(240)
    print "CompleteMessageTimeout has been set to: " + str(cmo.getCompleteMessageTimeout())

    print "Current IdleConnectionTimeout: " + str(cmo.getIdleConnectionTimeout())
    cmo.setIdleConnectionTimeout(240)
    print "IdleConnectionTimeout has been set to: " + str(cmo.getIdleConnectionTimeout())

    print "Current MaxMessageSize: " + str(cmo.getMaxMessageSize())
    cmo.setMaxMessageSize(50000000)
    print "MaxMessageSize has been set to: " + str(cmo.getMaxMessageSize())

    validate()
    save()
    print "\n"

activate()

disconnect()
exit()
