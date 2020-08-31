##################################################################################################################
#######################################Use below format to call the script########################################
#####<wlst.sh with full path> domain-details.py <console-username> <console-password> <admin-host> <admin-port>#####
##################################################################################################################
import sys
import os

#from subprocess import Popen,PIPE,STDOUT,call
#resp=Popen('hostname -f', shell=True, stdout=PIPE, )
#host = resp.communicate()[0].replace("\n","")
#print host
#outputFile = "/tmp/" + host + "-output.txt"

outputFile = "/tmp/domain-details.txt"

#Error message
def printException(message):
  print message
def extract(values):
  #print values
  returnVal = ""
  for value in values:
    returnVal = returnVal + " " + value.getName()
  return returnVal
#adminConnect method definition
def adminConnect(user, passwd, adminHost, adminPort):
  try:
    connect(user, passwd, 't3://' + adminHost + ':' + adminPort)
  except:
    message = "Unable to connect to AdminServer"
    printException(message)
def domainStats():
  domainName = cmo.getName()
  cd('/JTA/' + domainName)
  print "Domain:"
  print "  Name: " + domainName
  print "  JTATimeoutSeconds: " + str(cmo.getTimeoutSeconds())
  print "\n"
#serverStats method definition
def serverStats():
  cd('/')
  servers = cmo.getServers()
  domainRuntime()
  print "Servers:"
  for server in servers:
    sname = server.getName()
    print "  Name: " + sname
    cd('ServerRuntimes/' + sname)
    print "    ListenPort: " + str(cmo.getListenPort())
    cd('ServerRuntimes/' + sname + '/JVMRuntime/' + sname)
    print "    Heap(in GB): " + str(cmo.getHeapSizeCurrent()/(1024*1024*1024))
    print "    JavaVersion: " + str(cmo.getJavaVersion())
  #print "\n"
def fileStoreStats():
  serverConfig()
  print "File Stores:"
  fileStores = cmo.getFileStores()
  for fileStore in fileStores:
    fileStoreName = fileStore.getName()
    print "  Name: " + fileStoreName
    cd('/FileStores/' + fileStoreName)
    print "    MaxFileSize(in GB): " + str(cmo.getMaxFileSize()/(1024*1024*1024))
    #targets = extract(cmo.getTargets())
    #print "    Targets: " + targets
  print "\n"
def jdbcStoreStats():
  print "JDBC Stores:"
  cd('/')
  jdbcStores = cmo.getJDBCStores()
  for jdbcStore in jdbcStores:
    jdbcStoreName = jdbcStore.getName()
    print "  Name: " + jdbcStoreName
    cd('/JDBCStores/' + jdbcStoreName)
    print "    DataSource: " + str(cmo.getDataSource().getName())
    targets = extract(cmo.getTargets())
    print "    Targets: " + targets
  print "\n"
def jdbcSystemResourceStats():
  print "JDBC System Resources:"
  cd('/')
  jdbcResources = cmo.getJDBCSystemResources()
  for jdbcResource in jdbcResources:
    jdbcResourceName = jdbcResource.getName()
    print "  Name: " + jdbcResourceName
    #try:
    #  targets = extract(cmo.getTargets())
    #except:
    #  targets = "None"
    #  pass
    #print "    Targets: " + targets
    cd('/JDBCSystemResources/' + jdbcResourceName + '/JDBCResource/' + jdbcResourceName + '/JDBCConnectionPoolParams/' + jdbcResourceName)
    print "    MinCapacity: " + str(cmo.getMinCapacity())
    print "    MaxCapacity: " + str(cmo.getMaxCapacity())
    print "    StatementTimeout: " + str(cmo.getStatementTimeout())
  print "\n"
def jmsServerStats():
  print "JMS Servers:"
  cd('/')
  jmsServers = cmo.getJMSServers()
  for jmsServer in jmsServers:
    jmsServerName = jmsServer.getName()
    print "  Name: " + jmsServerName
    cd('/JMSServers/' + jmsServerName)
    persistentStoreName = cmo.getPersistentStore().getName()
    persistentStoreType = cmo.getPersistentStore().getType()
    print "    PersistenceStoreType: " + persistentStoreType
    if persistentStoreType == "JDBCStore" :
      cd('PersistentStore/' + persistentStoreName)
      print "      PrefixName: " + cmo.getPrefixName()
  print "\n"
def jmsResourceStats():
  print "JMS Modules:"
  cd('/')
  jmsModules = cmo.getJMSSystemResources()
  for jmsModule in jmsModules:
    jmsModuleName = jmsModule.getName()
    print "  Module: " + jmsModuleName
    cd('/JMSSystemResources/' + jmsModuleName)
    subDeploymentsArray = cmo.getSubDeployments()
    subDeployments = extract(subDeploymentsArray)
    print "    SubDeployments: " + subDeployments
    cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName)
    connectionFactories = cmo.getConnectionFactories()
    if len(connectionFactories) > 0:
      print "    ConnectionFactories: "
      for connectionFactory in connectionFactories:
        connectionFactoryName = connectionFactory.getName()
        print "      Name: " + connectionFactoryName
        #print pwd()
        #print "ConnectionFactories/" + connectionFactoryName
        cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/ConnectionFactories/' + connectionFactoryName)
        print "        JNDIName: " + cmo.getJNDIName()
    cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName)
    destinationKeys = cmo.getDestinationKeys()
    if len(destinationKeys) > 0:
      print "    DestinationKeys: " + str(destinationKeys)
    distributedQueues = cmo.getDistributedQueues()
    if len(distributedQueues) > 0:
      print "    DistributedQueues: "
      for distributedQueue in distributedQueues:
        distributedQueueName = distributedQueue.getName()
        print "      Name: " + distributedQueueName
        cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/DistributedQueues/' + distributedQueueName)
        print "        JNDIName: " + cmo.getJNDIName()
        distributedQueueMembers = cmo.getDistributedQueueMembers()
        if len(distributedQueueMembers) > 0:
          print "        DistributedQueueMembers: " + extract(distributedQueueMembers)
    cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName)
    distributedTopics = cmo.getDistributedTopics()
    if len(distributedTopics) > 0:
      print "    DistributedTopics: "
      for distributedTopic in distributedTopics:
        distributedTopicName = distributedTopic.getName()
        print "      Name: " + distributedTopicName
        cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/DistributedTopics/' + distributedTopicName)
        print "        JNDIName: " + cmo.getJNDIName()
        distributedTopicMembers = cmo.getDistributedTopicMembers()
        if len(distributedTopicMembers) > 0:
          print "        DistributedTopicMembers: " + extract(distributedTopicMembers)
    #cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName)
    #distributedTopics = cmo.getDistributedTopics()
    #if len(distributedTopics) > 0:
    #  print "    DistributedTopics: " + str(distributedTopics)
    cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName)
    foreignServers = cmo.getForeignServers()
    if len(foreignServers) > 0 :
      print "    ForeignServers: "
      for foreignServer in foreignServers:
        foreignServerName = foreignServer.getName()
        print "      Name: " + foreignServerName
    cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName)
    queues = cmo.getQueues()
    if len(queues) > 0:
      print "    Queues: "
      for queue in queues:
        queueName = queue.getName()
        print "      Name: " + queueName
        cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/Queues/' + queueName)
        print "        SubDeploymentName: " + cmo.getSubDeploymentName()
        cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/Queues/' + queueName + '/DeliveryParamsOverrides/' + queueName)
        print "        TimeToLive: " + str(cmo.getTimeToLive())
        print "        RedeliveryDelay: " + str(cmo.getRedeliveryDelay())
        cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/Queues/' + queueName + '/DeliveryFailureParams/' + queueName)
        print "        ExpirationPolicy: " + str(cmo.getExpirationPolicy())
        print "        RedeliveryLimit: " + str(cmo.getRedeliveryLimit())
    #cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName)
    #quotas = cmo.getQuotas()
    #if len(quotas) > 0:
    #  print "    Quotas: " + str(quotas)
    cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName)
    safErrorHandlings = cmo.getSAFErrorHandlings()
    if len(safErrorHandlings) > 0:
      print "    SAFErrorHandlings: "
      for safErrorHandling in safErrorHandlings:
        safErrorHandlingName = safErrorHandling.getName()
        print "      Name: " + safErrorHandlingName
    cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName)
    safImportedDestinations = cmo.getSAFImportedDestinations()
    if len(safImportedDestinations) > 0:
      print "    SAFImportedDestinations: "
      for safImportedDestination in safImportedDestinations:
        safImportedDestinationName = safImportedDestination.getName()
        print "      Name: " + safImportedDestinationName
    cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName)
    safRemoteContexts = cmo.getSAFRemoteContexts()
    if len(safRemoteContexts) > 0:
      print "    SAFRemoteContexts: "
      for safRemoteContext in safRemoteContexts:
        safRemoteContextName = safRemoteContext.getName()
        print "      Name: " + safRemoteContextName
    cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName)
    templates = cmo.getTemplates()
    if len(templates) > 0:
      print "    Templates: " + str(templates)
    cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName)
    topics = cmo.getTopics()
    if len(topics) > 0:
      print "    Topics: "
      for topic in topics:
        topicName = topic.getName()
        print "      Name: " + topicName
        cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/Topics/' + topicName)
        print "        SubDeploymentName: " + cmo.getSubDeploymentName()
        #print "        ConsumptionPausedAtStartup: " + cmo.getConsumptionPausedAtStartup()
        #print "        ProductionPausedAtStartup: " + cmo.getProductionPausedAtStartup()
    cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName)
    uniformDistributedQueues = cmo.getUniformDistributedQueues()
    if len(uniformDistributedQueues) > 0:
      print "    UniformDistributedQueues: "
      for uniformDistributedQueue in uniformDistributedQueues:
        uniformDistributedQueueName = uniformDistributedQueue.getName()
        print "      Name: " + uniformDistributedQueueName
    cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName)
    uniformDistributedTopics = cmo.getUniformDistributedTopics()
    if len(uniformDistributedTopics) > 0:
      print "    UniformDistributedTopics: "
      for uniformDistributedTopic in uniformDistributedTopics:
        uniformDistributedTopicName = uniformDistributedTopic.getName()
        print "      Name: " + uniformDistributedTopicName
  print "\n"
#Command line args validation
if len(sys.argv) != 5:
  message = "Irrelevant arguments passed to this script"
  printException(message)
else:
  user = sys.argv[1]
  passwd = sys.argv[2]
  adminHost = sys.argv[3]
  adminPort = sys.argv[4]

old_stdout = sys.stdout
sys.stdout = open(outputFile, 'w')

adminConnect(user, passwd, adminHost, adminPort)
domainStats()
serverStats()
fileStoreStats()
jdbcStoreStats()
jdbcSystemResourceStats()
jmsServerStats()
jmsResourceStats()

sys.stdout = old_stdout
os.system('chmod 777 ' + outputFile)
print "Script execution completed successfully"
print "Output has been written to " + outputFile

disconnect()
exit()

