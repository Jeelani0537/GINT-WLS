import sys
import commons
import wlstModule as wlm

adminHost = sys.argv[1]
adminPort = sys.argv[2]
managedHost = adminHost.replace("a01", "m01")
managedPort = '8001'
compositesList = sys.argv[10]

def retireComposite(managedHost, managedPort, user, passwd, compositeName, compositeVersion, compositePartition):
  print "-"*50
  wlm.sca_retireComposite(managedHost, managedPort, user, passwd, compositeName, compositeVersion, partition=compositePartition)
  print "-"*50
  print "\n"

def undeployComposite(managedHost, managedPort, user, passwd, compositeName, compositeVersion, compositePartition):
  print "-"*50
  url = "http://" + managedHost + ":" + managedPort
  wlm.sca_undeployComposite(url, compositeName, compositeVersion, partition=compositePartition)
  print "-"*50
  print "\n"

user,passwd = commons.readCredentials()
commons.adminConnect(user, passwd, host, port)

for composite in compositesList.split('\n'):
  composite = composite.replace(" ","")
  compositeProperties = composite.split(",")

  for compositeProperty in compositeProperties:
    if "name" in compositeProperty:
      compositeName = compositeProperty.split(":")[1]
    elif "version" in compositeProperty:
      compositeVersion = compositeProperty.split(":")[1]
    elif "partition" in compositeProperty:
      compositePartition = compositeProperty.split(":")[1]
    elif "action" in compositeProperty:
      compositeAction = compositeProperty.split(":")[1]
  
  if compositeAction == 'retire':
    retireComposite(managedHost, managedPort, user, passwd, compositeName, compositeVersion, compositePartition)
  elif compositeAction == 'undeploy':
    undeployComposite()
  else:
    print "Invalid action: " + compositeAction + " for " + compositeName

commons.disconnectWithSuccess()
commons.exitWithSuccess()
