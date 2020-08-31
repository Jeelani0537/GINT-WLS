#source boot.properties
#/opt/oracle/FMW12.2/oracle_common/common/bin/wlst.sh DBFSToNetAPPMigrate.py $password CMOWD2249 12.2 cmcnchn-lx4047.ikeadt.com 7001 soa

import sys
import commons
import wlstModule as wlm

adminHost = sys.argv[1]
adminPort = sys.argv[2]
stack = sys.argv[6]
fmwVersion = sys.argv[7]
domainName = sys.argv[9]

def createFS(fileStoreName, commonMount, domainName, serverName, cacheDir):
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
  wlm.set('Targets',jarray.array([ObjectName('com.bea:Name=' + serverName + ' (migratable),Type=MigratableTarget')], ObjectName))

  print "Setting synchronous write policy to: Direct-Write-With-Cache"
  wlm.cmo.setSynchronousWritePolicy('Direct-Write-With-Cache')

  print "Setting cache directory to: " + cacheDir
  wlm.cmo.setCacheDirectory(cacheDir)

def jmsServerPersistentStoreUpdate(jmsServerName, fileStoreName):
  wlm.cd('/JMSServers/' + jmsServerName)
  print "Updating " + jmsServerName + " persistent store to: "+ fileStoreName
  wlm.cmo.setPersistentStore(wlm.getMBean('/FileStores/' + fileStoreName))
  print "Updating " + jmsServerName + "'s maximum message size to: 16000000"
  wlm.cmo.setMaximumMessageSize(16000000)

def serverDefaultStoreUpdate(serverName, commonMount, tLogDirectory, cacheDir):
  print "Enabling default store"
  wlm.cd('/Servers/' + serverName + '/TransactionLogJDBCStore/' + serverName)
  wlm.cmo.setEnabled(false)

  wlm.cd('/Servers/'+ serverName + '/DefaultFileStore/' + serverName)
  print "Configuring directory to: " + tLogDirectory
  wlm.cmo.setDirectory(tLogDirectory)

  print "Configuring SynchronousWritePolicy to: Direct-Write-With-Cache"
  wlm.cmo.setSynchronousWritePolicy('Direct-Write-With-Cache')

  print "Configuring cache directory to: " + cacheDir
  wlm.cmo.setCacheDirectory(cacheDir)

def detachJDBCStoreFromJMSServer(jdbcStoreName):
  if wlm.getMBean('/JDBCStores/' + jdbcStoreName):
    wlm.cd('/JDBCStores/' + jdbcStoreName)
    print "Removing targets from: " + jdbcStoreName
    wlm.set('Targets',jarray.array([], ObjectName))
  else:
    print jdbcStoreName + " is not found"

#def validateSAFAgents(commonMount, domainName, serverName, cacheDir):
#  cd('/')
#  sAgents = cmo.getSAFAgents()
#  for sAgent in sAgents:
#    sAgentName = sAgent.getName()
#    cd('/SAFAgents/' + sAgentName)
#    store = cmo.getStore().getName()
#    if "JDBC" in store:
#      fileStore = store.replace("JDBC", "File")
#      createFS(fileStore, commonMount, domainName, serverName, cacheDir)
#      print sAgentName + " is associated with " + store + ". Changing it to " + fileStore
#      cmo.setStore(getMBean('/FileStores/' + fileStore))

def createResources():
  for server in servers:
    print "----------------------------------------------------------------------------------"
    serverName = server.getName()
    if serverName != "AdminServer" :
      serverIndex = serverName[-1]
      stackCaps = serverName[0:3].upper()
      fileStoreName = "WL" + stackCaps + "FileStore-" + serverIndex
      jdbcStoreName = "WL" + stackCaps + "JDBCStore-" + serverIndex
      jmsServerName = "WL" + stackCaps + "JMSServer-" + serverIndex
      tLogDirectory = "/" + commonMount + "/" + domainName + "/TLOG/TLOG_" + serverName
      cacheDir = "/opt/oracle/domains" + fmwVersion + "/" + domainName + "/servers/" + serverName + "/tmp"

      createFS(fileStoreName, commonMount, domainName, serverName, cacheDir)
      jmsServerPersistentStoreUpdate(jmsServerName, fileStoreName)
      #serverDefaultStoreUpdate(serverName, commonMount, tLogDirectory, cacheDir)
      detachJDBCStoreFromJMSServer(jdbcStoreName)
      #validateSAFAgents(commonMount, domainName, serverName, cacheDir)
    else:
      print "Found AdminServer. No action required"
    print "----------------------------------------------------------------------------------"
    print "\n"

if stack == "odi" or stack == "bam":
  print "This is not meant for " + stack + " stack. Exiting..."
  exit()

user,passwd = commons.readCredentials()
commons.adminConnect(user, passwd, adminHost, adminPort)

servers = wlm.cmo.getServers()
if stack == "soa" :
  commonMount = "oitp_soa"
elif stack == "osbgtw" :
  commonMount = "oitp_osb"

commons.takeSession()

createResources()

commons.activateChanges()
commons.disconnectWithSuccess()
commons.exitWithSuccess()
