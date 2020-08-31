##Run script in below format
##/opt/oracle/FMW11.1.1.7/oracle_common/common/bin/wlst.sh soa-infra-status.py weblogic <password> cfseelm-lx4159.ikeadt.com 7001

user = sys.argv[1]
passwd = sys.argv[2]
adminHost = sys.argv[3]
adminPort = sys.argv[4]
#servers = sys.argv[5]

#print user

connect(user,passwd,'t3://' + adminHost + ':' + adminPort)

servers = cmo.getServers()

domainRuntime()
cd ("/AppRuntimeStateRuntime/AppRuntimeStateRuntime")

for server in servers:
  serverName = str(server.getName())
  if serverName != "AdminServer" :
    print "soa-infra status on " + serverName + ":" + cmo.getCurrentState("soa-infra", serverName)

