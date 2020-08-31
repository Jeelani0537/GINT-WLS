#############################################################################################
#Prepared by: Praveen Raj Kumar Kandregula
#Purpose: This checks health of a domain through WLST.
#############################################################################################

import sys
import commons

details = eval(sys.argv[1])
outputFile = sys.argv[2]
domainId = sys.argv[3]
output = "\n"

def serversStatus(user, passwd, host, port, output, domainName, domainId):
  output = output + "-"*60 + "\n"
  #output = output + domainName + ": \n"
  output = output + domainId + " -- " + domainName + ": \n"
  try:
    connect(user, passwd, "t3://" + host + ":" + port, timeout="30000")
    serversList = cmo.getServers()
    domainName = cmo.getName()
    domainRuntime()
    for server in serversList:
      sname = server.getName()
      try:
        cd('/ServerRuntimes/' + str(sname))
        overallHealth = str(cmo.getOverallHealthState())
      except:
        overallHealth = "State:UNREACHABLE"
      for item in overallHealth.split(","):
        if 'State' in item:
          state, health = item.split(":")
          output = output + str(sname) + ": " + health + "\n"
    disconnect()
    #output = output + "-"*60 + "\n"
  except:
    print "Unable to connect to AdminServer on " + host
    output = output + "Unable to connect to AdminServer\n"

  output = output + "-"*60 + "\n"
  return output

user,passwd = commons.readCredentials()

for item in details:
  host = details[item]['host']
  port = details[item]['port']
  output = serversStatus(user, passwd, host, port, output, item, domainId)

print output

old_stdout = sys.stdout
sys.stdout = open(outputFile, 'a+')
print output

sys.stdout = old_stdout
exit()
