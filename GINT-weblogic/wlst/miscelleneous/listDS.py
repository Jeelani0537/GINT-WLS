##################################################################################################################
#######This script has been prepared to identify whether a DS is connecting through OID or traditional JDBC#######
#########DS connecting through OID will not have their connection strings printed by nature of this script########
#######################################Use below format to call this script#######################################
############<wlst.sh full path> listDS.py <console-user> <console-password> <Admin-Host> <Admin-Port>#############

if len(sys.argv) != 5:
  print "Invalid usage of script"
  print "Use below format to call this script.\n<wlst.sh full path> listDS.py <console-user> <console-password> <Admin-Host> <Admin-Port>"
  exit()
  
user = sys.argv[1]
passwd = sys.argv[2]
adminHost = sys.argv[3]
adminPort = sys.argv[4]

try:
  connect(user, passwd, 't3://' + adminHost + ':' + adminPort)
except:
  print "Unable to connect to AdminServer"
  exit()
  
dataSources = cmo.getJDBCSystemResources()
for ds in dataSources:
  dsName = ds.getName()
  cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName)
  connUrl = cmo.getUrl()
  #print dsName + "," + connUrl
  if "ldap" in connUrl :
    serviceName = connUrl.split(",cn")[0].split("/")[-1]
    print serviceName + " , " + dsName + " , OID , " + connUrl
  elif "SERVICE_NAME" in connUrl:
    serviceName = connUrl.split("SERVICE_NAME")[1].replace("=","").split(")")[0].replace(" ","")
    print serviceName + " , " + dsName + " , JDBC , " + connUrl
  else:
    serviceName = connUrl.split("/")[-1]
    print serviceName + " , " + dsName + " , JDBC , " + connUrl
  #print dsName + "," + connUrl + "," + serviceName

disconnect()
exit()
