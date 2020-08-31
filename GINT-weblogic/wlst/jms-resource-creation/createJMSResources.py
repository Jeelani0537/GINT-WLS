import sys

#Properties being passed to this script should be of this format. This format is bound to change as per the requirement later
keys = "Type(Queue/Topic),Name,jmsModule,jndiName,subDeployment,expirationPolicy,errorDestination,timeToLiveOverride,redeliveryDelayOverride,redeliveryLimit,forwardingPolicy"
dictKeys = ["Type", "Name", "jmsModule", "jndiName", "subDeployment", "expirationPolicy", "errorDestination", "timeToLiveOverride", "redeliveryDelayOverride", "redeliveryLimit", "forwardingPolicy"]
dictResources = {}

#Methods definition
def exitWithError(message):
  print message
  exit()

def adminConnect(user, passwd, adminHost, adminPort):
  try:
    connect(user, passwd, "t3://" + adminHost + ":" + adminPort)
  except:
    message = "==>Unable to connect to admin server"
    exitWithError(message)

def createJMSResource(dictResources):
  print dictResources
  restype = dictResources['Type'].replace(" ","")
  resourceName = dictResources['Name'].replace(" ","")
  moduleName = dictResources['jmsModule'].replace(" ","")
  jndiName = dictResources['jndiName'].replace(" ","")
  sdName = dictResources['subDeployment'].replace(" ","")
  expirationPolicy = dictResources['expirationPolicy'].replace(" ","")
  errorDestination = dictResources['errorDestination'].replace(" ","")
  timeToLiveOverride = dictResources['timeToLiveOverride']
  redeliveryDelayOverride = dictResources['redeliveryDelayOverride']
  redeliveryLimit = dictResources['redeliveryLimit']
  forwardingPolicy = dictResources['forwardingPolicy'].replace(" ","")

  #if restype.lower() != "queue" or restype.lower() != "topic":
  #  message = "Invalid restype found for " + str(dictResources)
  #  exitWithError(message)
  #JMS Server validation
  if not getMBean('/JMSSystemResources/' + moduleName):
    message = "==>" + moduleName + " doesn't exist"
    exitWithError(message)
  #Subdeployment validation
  if not getMBean('/JMSSystemResources/' + moduleName + '/SubDeployments/' + sdName):
    message = "==>" + sdName + "doesn't exist"
    exitWithError(message)

  print "==============================================================================================="
  if restype.lower() == "queue" :
    resourceType = "UniformDistributedQueue"
  elif restype.lower() == "topic":
    resourceType = "UniformDistributedTopic"

  #Resource validation
  if not getMBean('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/' + resourceType + 's/' + resourceName):
    print resourceName + " doesn't exist !!"
    #Creation
    print "Adding " + resourceName
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName )
    if restype.lower() == "queue" :
      cmo.createUniformDistributedQueue(resourceName)
    elif restype.lower() == "topic":
      cmo.createUniformDistributedTopic(resourceName)
    print resourceName + " has been created"

    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/' + resourceType + 's/' + resourceName)
    cmo.setJNDIName(jndiName)
    print "JNDI Name " + jndiName + " has been set"

    if restype.lower() == "topic":
      cmo.setForwardingPolicy(forwardingPolicy)

    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/' + resourceType + 's/' + resourceName)
    cmo.setSubDeploymentName(sdName)
    print "Subdeployment " + sdName + " has been assigned"

    if timeToLiveOverride != "NULL":
      cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/' + resourceType + 's/' + resourceName + '/DeliveryParamsOverrides/' + resourceName)
      cmo.setTimeToLive(long(timeToLiveOverride))
      print "TimeToLiveOverride " + str(timeToLiveOverride) + " has been set"

    if redeliveryDelayOverride != "NULL":
      cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/' + resourceType + 's/' + resourceName + '/DeliveryParamsOverrides/' + resourceName)
      cmo.setRedeliveryDelay(int(redeliveryDelayOverride))
      print "RedeliveryDelayOverride " + str(redeliveryDelayOverride) + " has been set"
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/' + resourceType + 's/' + resourceName + '/DeliveryFailureParams/' + resourceName)

    if redeliveryLimit != "NULL":
      cmo.setRedeliveryLimit(int(redeliveryLimit))
      print "RedeliveryLimit " + str(redeliveryLimit) + " has been set"
    if expirationPolicy != "NULL":
      cmo.setExpirationPolicy(expirationPolicy)
      print "ExpirationPolicy " + expirationPolicy + " has been set"
      cmo.setErrorDestination(getMBean('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/UniformDistributedQueues/' + errorDestination))
      print "ErrorDestination " + errorDestination + " has been set"
  else:
    print resourceName + " exists !!!"
  
  print "===============================================================================================\n\n"

#Reading properties file
try:
  propertiesFile = sys.argv[1]
  print "==>Properties file has been identified...\n\n"
except:
  message = "==>Invalid usage of script. Run the script in below format \n==><wlst.sh with full path> createJMSResources.py <resources properties file with full path> <console-username> <console-password> <admin-host> <admin-port>"
  exitWithError(message)

#Command line args validation
if len(sys.argv) != 6 :
  message = "==>Invalid usage of script. Run the script in below format \n==><wlst.sh with full path> createJMSResources.py <resources properties file with full path> <console-username> <console-password> <admin-host> <admin-port>"
  exitWithError(message)
else:
  #Reading command line variables
  user = sys.argv[2]
  passwd = sys.argv[3]
  adminHost = sys.argv[4]
  adminPort = sys.argv[5]

  #Read csv properties file
  f = open(propertiesFile)
  header = f.readline().lower()
  resources = f.readlines()

  #Properties file header validation
  if header.replace("\n","") != keys.lower() :
    message = "==>Invalid header found in properties file"
    exitWithError(message)
  else:
    #Connect to admin server
    adminConnect(user, passwd, adminHost, adminPort)

    try:
      edit()
      startEdit()
    except:
      errorMessage = "Unable to take session. See if there are ny open sessions"
      exitWithError(errorMessage)

    for resource in resources:
      resource = resource.replace("\n","")
      if resource.endswith(","):
        resource = resource + "NULL"
      resource = resource.replace(",,",",NULL,")
      flag = 0
      for item in resource.split(","):
        if item == "":
          item = "NULL"
        dictResources[dictKeys[flag]] = item
        flag = flag + 1

      #Call JMS Resource Creation method
      createJMSResource(dictResources)

  validate()
  save()
  activate()
  disconnect()
  exit()

