#############################################################################################
#Prepared by : Praveen Raj Kumar Kandregula
#Purpose     : This has been prepared to migrate bam related jms resources from jdbc store to
#              filestore across all 12C SOA and OSB domains. These resources will get created
#              in their absence.
#Resources   :
#  SOA       : MigratableTarget, JMSServers, FilePersistenceStore, SubDeployment,
#              ConnectionFactory-nonxa, queue
#  OSB       : MigratableTarget, JMSServers, FilePersistenceStore, SubDeployment,
#              ConnectionFactory-xa, queue, SAFAgent
#Process to
#    execute : /opt/oracle/FMW12.2/oracle_common/common/bin/wlst.sh bam-jms-resources.py \
#              ptseelm-lx41463.ikeadt.com 7001 dummy dummy dummy soa 12.2 loginURL
#############################################################################################

import sys
import commons
import wlstModule as wlm

adminHost = sys.argv[1]
adminPort = sys.argv[2]
stack = sys.argv[6]
fmwVersion = sys.argv[7]
loginURL = sys.argv[8]

def createMigratableTarget(migratableTargetName, clusterName, serverName):
  print '\n'
  wlm.cd('/')

  if wlm.getMBean('/MigratableTargets/' + migratableTargetName):
    print migratableTargetName + " exists already"
  else:
    print migratableTargetName + " is being created"
    wlm.cmo.createMigratableTarget(migratableTargetName)

  wlm.cd('/MigratableTargets/' + migratableTargetName)
  print "Targets are being set to: " + clusterName
  wlm.cmo.setCluster(wlm.getMBean('/Clusters/' + clusterName))

  print "Preferred server is being set to: " + serverName
  wlm.cmo.setUserPreferredServer(wlm.getMBean('/Servers/' + serverName))

  print "Migration policy is being set to: manual"
  wlm.cmo.setMigrationPolicy('manual')
  print '\n'

def createFS(fileStoreName, commonMount, domainName, migratableTargetName, cacheDir, serverName):
  print '\n'
  wlm.cd('/')

  if wlm.getMBean('/FileStores/' + fileStoreName):
    print fileStoreName + " exists already"
  else:
    print fileStoreName + " is being created"
    wlm.cmo.createFileStore(fileStoreName)

  wlm.cd('/FileStores/' + fileStoreName)
  directory = '/' + commonMount + '/' + domainName + '/JMS/' + serverName
  print "Directory is being set to: " +  directory
  wlm.cmo.setDirectory(directory)

  wlm.set('Targets',jarray.array([ObjectName('com.bea:Name=' + migratableTargetName + ',Type=MigratableTarget')], ObjectName))
  print "Setting synchronous write policy to: Direct-Write-With-Cache"
  wlm.cmo.setSynchronousWritePolicy('Direct-Write-With-Cache')

  print "Setting cache directory to: " + cacheDir
  wlm.cmo.setCacheDirectory(cacheDir)
  print '\n'

def jmsServerPersistentStoreUpdate(jmsServerName, fileStoreName, serverName, migratableTargetName):
  print '\n'
  wlm.cd('/')

  if wlm.getMBean('/JMSServers/' + jmsServerName):
    print jmsServerName + " exists already"
  else:
    print jmsServerName + " is being created"
    wlm.cmo.createJMSServer(jmsServerName)

  wlm.cd('/JMSServers/' + jmsServerName)
  print "Updating " + jmsServerName + " persistent store to: "+ fileStoreName
  print wlm.cmo.getPersistentStore()

  print "Setting PersistentStore to: " + fileStoreName
  wlm.cmo.setPersistentStore(wlm.getMBean('/FileStores/' + fileStoreName))

  print "Updating " + jmsServerName + "'s maximum message size to: 16000000"
  wlm.cmo.setMaximumMessageSize(16000000)

  wlm.set('Targets',jarray.array([ObjectName('com.bea:Name=' + migratableTargetName + ',Type=MigratableTarget')], ObjectName))
  print '\n'

def createSAFAgent(safAgentName, migratableTargetName, fileStoreName):
  print '\n'
  wlm.cd('/')

  if wlm.getMBean('/SAFAgents/' + safAgentName):
    print safAgentName + "exists"
  else:
    print safAgentName + " is being created"
    wlm.cmo.createSAFAgent(safAgentName)

  wlm.cd('/SAFAgents/' + safAgentName)
  print "Targets are being set to: " + migratableTargetName
  wlm.set('Targets',jarray.array([ObjectName('com.bea:Name=' + migratableTargetName + ',Type=MigratableTarget')], ObjectName))

  print "Setting PersistentStore to: " + fileStoreName
  wlm.cmo.setStore(wlm.getMBean('/FileStores/' + fileStoreName))

  print "ServiceType is being set to: Sending-only"
  wlm.cmo.setServiceType('Sending-only')

  wlm.cd('/SAFAgents/' + safAgentName + '/JMSSAFMessageLogFile/' + safAgentName)  
  wlm.cmo.setFileName('logs/safagents/' + safAgentName + '/jms.messages.log')
  print '\n'

def createJMSSubDeployment(subDeploymentName, servers, stackCaps):
  print '\n'
  wlm.cd('/')

  if wlm.getMBean('JMSSystemResources/oitp_bam'):
    print "oitp_bam jms module exists"
    wlm.cd('/JMSSystemResources/oitp_bam')

    if wlm.getMBean('/JMSSystemResources/oitp_bam/SubDeployments/' + subDeploymentName):
      print subDeploymentName + " exists"
    else:
      print "Subdeployment " + subDeploymentName + " is being created"
      wlm.cmo.createSubDeployment(subDeploymentName)

    wlm.cd('/JMSSystemResources/oitp_bam/SubDeployments/' + subDeploymentName)
    objects = []

    for server in servers:
      serverName = server.getName()
      if 'Admin' not in serverName and stackCaps == "OSB" and subDeploymentName != "BAMOSBDistributedSubDeployment":
        serverIndex = serverName[-1]
        objects.append(ObjectName('com.bea:Name=BAMSAFAgent-' + serverIndex + ',Type=SAFAgent'))
      elif 'Admin' not in serverName and (stackCaps == "SOA" or subDeploymentName == "BAMOSBDistributedSubDeployment"):
        serverIndex = serverName[-1]
        objects.append(ObjectName('com.bea:Name=BAM' + stackCaps + 'JMSServer-' + serverIndex + ',Type=JMSServer'))

    print subDeploymentName + " targets are being set to: " + str(objects)
    wlm.set('Targets',jarray.array(objects, ObjectName))
  else:
    print "oitp_bam jms module doesn't exist"
    errorMessage = "oitp_bam jms module doesn't exist!!!"
    commons.exitWithError(errorMessage)
  print '\n'

def createJMSCF(connectionFactoryName, xaEnabled, subDeploymentName, stackCaps):
  print '\n'
  wlm.cd('/JMSSystemResources/oitp_bam/JMSResource/oitp_bam')

  if wlm.getMBean('/JMSSystemResources/oitp_bam/JMSResource/oitp_bam/ConnectionFactories/' + connectionFactoryName):
    print connectionFactoryName + " exists in oitp_bam. Deleting it"
    wlm.cmo.destroyConnectionFactory(wlm.getMBean('/JMSSystemResources/oitp_bam/JMSResource/oitp_bam/ConnectionFactories/' + connectionFactoryName))
  
  print connectionFactoryName + " is being created"
  wlm.cmo.createConnectionFactory(connectionFactoryName)

  wlm.cd('/JMSSystemResources/oitp_bam/JMSResource/oitp_bam/ConnectionFactories/' + connectionFactoryName)
  print "JNDI name of " + connectionFactoryName + " is being set to: jms/" + connectionFactoryName
  wlm.cmo.setJNDIName('jms/' + connectionFactoryName)

  wlm.cd('/JMSSystemResources/oitp_bam/JMSResource/oitp_bam/ConnectionFactories/' + connectionFactoryName + '/ClientParams/' + connectionFactoryName)
  print "ClientIdPolicy of " + connectionFactoryName + " is being set to: Restricted"
  wlm.cmo.setClientIdPolicy('Restricted')

  print "SubscriptionSharingPolicy of " + connectionFactoryName + " is being set to: Exclusive"
  wlm.cmo.setSubscriptionSharingPolicy('Exclusive')

  print "MessagesMaximum of " + connectionFactoryName + " is being set to: 10"
  wlm.cmo.setMessagesMaximum(10)

  wlm.cd('/JMSSystemResources/oitp_bam/JMSResource/oitp_bam/ConnectionFactories/' + connectionFactoryName + '/TransactionParams/' + connectionFactoryName)
  print "XAConnectionFactory of " + connectionFactoryName + " is being set to: " + str(xaEnabled)
  wlm.cmo.setXAConnectionFactoryEnabled(xaEnabled)

  wlm.cd('/JMSSystemResources/oitp_bam/JMSResource/oitp_bam/ConnectionFactories/' + connectionFactoryName)
  if stackCaps == "SOA":
    wlm.cmo.setDefaultTargetingEnabled(false)
    print "subDeployment of " + connectionFactoryName + " is being set to: " + subDeploymentName
    wlm.cmo.setSubDeploymentName(subDeploymentName)
  elif stackCaps == "OSB":
    print "Enabling default taregting for: " + connectionFactoryName
    wlm.cmo.setDefaultTargetingEnabled(true)
  print '\n'

def createJMSDistributedQueue(queueName, subDeploymentName):
  print '\n'
  wlm.cd('/JMSSystemResources/oitp_bam/JMSResource/oitp_bam')

  if wlm.getMBean('/JMSSystemResources/oitp_bam/JMSResource/oitp_bam/UniformDistributedQueues/' + queueName):
    print queueName + " exists in oitp_bam"
  else:
    print queueName + " is being created in oitp_bam"
    wlm.cmo.createUniformDistributedQueue(queueName)

  wlm.cd('/JMSSystemResources/oitp_bam/JMSResource/oitp_bam/UniformDistributedQueues/' + queueName)
  print "JNDI name of " + queueName + " is being set to: jms/" + queueName
  wlm.cmo.setJNDIName('jms/' + queueName)

  wlm.cd('/JMSSystemResources/oitp_bam/JMSResource/oitp_bam/UniformDistributedQueues/' + queueName)
  print "subDeployment of " + queueName + " is being set to: " + subDeploymentName
  wlm.cmo.setSubDeploymentName(subDeploymentName)
  print '\n'

def createRemoteSAFContext(jmsModuleName, remoteSAFContextName, loginURL, bamUser, bamPassword):
  print '\n'
  if wlm.getMBean('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFRemoteContexts/' + remoteSAFContextName):
    print remoteSAFContextName + " exists"
  else:
    wlm.cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName)
    print remoteSAFContextName + " is being created"
    wlm.cmo.createSAFRemoteContext(remoteSAFContextName)
  
  wlm.cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFRemoteContexts/' + remoteSAFContextName + '/SAFLoginContext/' + remoteSAFContextName)
  print "Login URL is being set to: " + loginURL
  wlm.cmo.setLoginURL(loginURL)

  print "User is being set to: " + bamUser
  wlm.cmo.setUsername(bamUser)
  wlm.cmo.setPassword(bamPassword)
  print '\n'
    
def createSAFErrorHandling(jmsModuleName,safErrorHandlerName):
  print '\n'
  if wlm.getMBean('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFErrorHandlings/' + safErrorHandlerName):
    print safErrorHandlerName + " exists"
  else:
    wlm.cd('/JMSSystemResources/' + jmsModuleName  + '/JMSResource/' + jmsModuleName)
    print safErrorHandlerName + " is being created"
    wlm.cmo.createSAFErrorHandling(safErrorHandlerName)

  wlm.cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFErrorHandlings/' + safErrorHandlerName)
  print "Policy is being set to: Always-Forward" 
  wlm.cmo.setPolicy('Always-Forward')
  print '\n'

def createSAFImportedDestinations(jmsModuleName, safImportedDestinations, remoteSAFContextName, safErrorHandlerName, subDeploymentName, transactionErrorQueue, topics):
  print '\n'
  if wlm.getMBean('/JMSSystemResources/' + jmsModuleName  + '/JMSResource/' + jmsModuleName + '/SAFImportedDestinations/' + safImportedDestinations):
    print safImportedDestinations + " exists"
  else:
    print safImportedDestinations + " is being created"
    wlm.cd('/JMSSystemResources/' + jmsModuleName  + '/JMSResource/' + jmsModuleName)
    wlm.cmo.createSAFImportedDestinations(safImportedDestinations)

  wlm.cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFImportedDestinations/' + safImportedDestinations)
  print "JNDIPrefix is being set to: saf/"
  wlm.cmo.setJNDIPrefix('saf/')

  print "SAFRemoteContext for " + safImportedDestinations + " is being set to: " + remoteSAFContextName
  wlm.cmo.setSAFRemoteContext(wlm.getMBean('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFRemoteContexts/' + remoteSAFContextName))

  print "SAFErrorHandling for " +  safImportedDestinations + " is being set to: " + safErrorHandlerName
  wlm.cmo.setSAFErrorHandling(wlm.getMBean('/JMSSystemResources/'+ jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFErrorHandlings/' + safErrorHandlerName))
  wlm.cmo.setTimeToLiveDefault(-1)

  print "Subdeployment for " +  safImportedDestinations + " is being set to: " + subDeploymentName
  wlm.cmo.setSubDeploymentName(subDeploymentName)

  if wlm.getMBean('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFImportedDestinations/' + safImportedDestinations + "/SAFQueues/" + transactionErrorQueue):
    print "SAFQueue: " + transactionErrorQueue + " exists"
  else:
    wlm.cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFImportedDestinations/' + safImportedDestinations)
    print "SAFQueue: " + transactionErrorQueue + " is being created"
    wlm.cmo.createSAFQueue(transactionErrorQueue)

  wlm.cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFImportedDestinations/' + safImportedDestinations + "/SAFQueues/" + transactionErrorQueue)
  print "Remote JNDI is being set to: jms/" + transactionErrorQueue
  wlm.cmo.setRemoteJNDIName('jms/' + transactionErrorQueue)

  print "ErrorHandler for " + transactionErrorQueue + " is being set to: " + safErrorHandlerName
  wlm.cmo.setSAFErrorHandling(wlm.getMBean('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFErrorHandlings/' + safErrorHandlerName))

  print "Local JNDI is being set to: jms/" + transactionErrorQueue
  wlm.cmo.setLocalJNDIName('jms/' + transactionErrorQueue)

  for topic in topics.split(','):
    if wlm.getMBean('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFImportedDestinations/' + safImportedDestinations + "/SAFTopics/" + topic):
      print "SAFTopic: " + topic + " exists"
    else:
      wlm.cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFImportedDestinations/' + safImportedDestinations)
      print "SAFTopic: " + topic + " is being created"
      wlm.cmo.createSAFTopic(topic)

    wlm.cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFImportedDestinations/' + safImportedDestinations + "/SAFTopics/" + topic)
    jndiName = "jms/" + topic.replace("SAF_","")
    print "Remote JNDI is being set to: " + jndiName
    wlm.cmo.setRemoteJNDIName(jndiName)

    print "ErrorHandler for " + topic + " is being set to: " + safErrorHandlerName
    wlm.cmo.setSAFErrorHandling(wlm.getMBean('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFErrorHandlings/' + safErrorHandlerName))

    print "Local JNDI is being set to: " + jndiName
    wlm.cmo.setLocalJNDIName(jndiName)

  wlm.cd('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFErrorHandlings/' + safErrorHandlerName)
  print "ErrorDestination for: " + safErrorHandlerName + " is being set to: " + transactionErrorQueue
  wlm.cmo.setSAFErrorDestination(wlm.getMBean('/JMSSystemResources/' + jmsModuleName + '/JMSResource/' + jmsModuleName + '/SAFImportedDestinations/' + safImportedDestinations + "/SAFQueues/" + transactionErrorQueue))

  print '\n'

def createResources(servers, commonMount, domainName, fmwVersion, clusterName, xaEnabled, bamPassword, cfName, queueName):
  for server in servers:
    print "----------------------------------------------------------------------------------"
    serverName = server.getName()
    if serverName != "AdminServer" :
      serverIndex = serverName[-1]
      stackCaps = serverName[0:3].upper()
      fileStoreName = "BAM" + stackCaps + "FileStore-" + serverIndex
      jdbcStoreName = "BAM" + stackCaps + "JDBCStore-" + serverIndex
      jmsServerName = "BAM" + stackCaps + "JMSServer-" + serverIndex
      safAgentName = "BAMSAFAgent-" + serverIndex

      tLogDirectory = "/" + commonMount + "/" + domainName + "/TLOG/TLOG_" + serverName
      cacheDir = "/opt/oracle/domains" + fmwVersion + "/" + domainName + "/servers/" + serverName + "/tmp"
      migratableTargetName = "bam_jmsserver" + serverIndex + "(migratable)"

      createMigratableTarget(migratableTargetName, clusterName, serverName)
      createFS(fileStoreName, commonMount, domainName, migratableTargetName, cacheDir, serverName)
      jmsServerPersistentStoreUpdate(jmsServerName, fileStoreName, serverName, migratableTargetName)

      if stackCaps == "OSB":
        createSAFAgent(safAgentName, migratableTargetName, fileStoreName)
    else:
      print "Found AdminServer. No action required"
    print "----------------------------------------------------------------------------------"
    print "\n"

  createJMSSubDeployment('BAMDistributedSubDeployment', servers, stackCaps)
  createJMSCF(cfName, xaEnabled, 'BAMDistributedSubDeployment', stackCaps)

  if stackCaps == "SOA":
    createJMSDistributedQueue(queueName, 'BAMDistributedSubDeployment')
  elif stackCaps == "OSB":
    createJMSSubDeployment('BAMOSBDistributedSubDeployment', servers, stackCaps)
    createJMSDistributedQueue(queueName, 'BAMOSBDistributedSubDeployment')
    createRemoteSAFContext('oitp_bam', 'BAMRemoteSAFContext', loginURL, 'bamuser', bamPassword)
    createSAFErrorHandling('oitp_bam', 'BAMSAFErrorHandling')
    createSAFImportedDestinations('oitp_bam', 'BAMSAFImportedDestinations', 'BAMRemoteSAFContext', 'BAMSAFErrorHandling', 'BAMDistributedSubDeployment', 'BAM_TRANSACTION_ERRORQUEUE', 'SAF_BAM_UTILITY_SERIVCE_TOPIC,SAF_BAM_UTILITY_SERVICE_BUSINESS_OBJECTS_TOPIC')

  print "\n\n"

if stack == "odi" or stack == "bam" :
  print "This is not meant for " + stack + " stack. Exiting..."
  exit()

user,passwd = commons.readCredentials()
bamUserPassword = commons.readBamPassword()
commons.adminConnect(user, passwd, adminHost, adminPort)

servers = wlm.cmo.getServers()
domainName = wlm.cmo.getName()

if stack == "soa" :
  commonMount = "oitp_soa"
  clusterName = "soa_cluster1"
  xaEnabled = false
  cfName = "BAM_UTILITY_SERVICE_CF"
  queueName = "BAM_UTILITY_SERVICE_QUEUE"
elif stack == "osbgtw" :
  commonMount = "oitp_osb"
  clusterName = "osb_cluster1"
  xaEnabled = true
  cfName = "BAM_UTILITY_CF"
  queueName = "BAM_UTILITY_TRAN_QUEUE"

commons.takeSession()

createResources(servers, commonMount, domainName, fmwVersion, clusterName, xaEnabled, bamUserPassword, cfName, queueName)

commons.activateChanges()
commons.disconnectWithSuccess()
commons.exitWithSuccess()
