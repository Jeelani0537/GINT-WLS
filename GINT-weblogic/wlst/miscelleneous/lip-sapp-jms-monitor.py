#source /opt/oracle/domains11.1.1.9/LIP222/servers/AdminServer/security/boot.properties && /opt/oracle/middleware/oracle_common/common/bin/wlst.sh jmsMonitor.py $password LIP222 11.1.1.9 lipp-de-sto-00222-a01.ikea.com 9001
#source /opt/oracle/domains11.1.1.9/SAPP222/servers/AdminServer/security/boot.properties && /opt/oracle/middleware/oracle_common/common/bin/wlst.sh jmsMonitor.py $password SAPP222 11.1.1.9 sapp-de-sto-00222-a01.ikea.com 8001

enpasswd = sys.argv[1]
domainName = sys.argv[2]
fmwVersion = sys.argv[3]
adminHost = sys.argv[4]
adminPort = sys.argv[5]

#Debug while exit
def exitWithError(errorMessage):
  print "Script execution failed !!!" + errorMessage
  exit()

#This function will decrypt and returns encrypted value
def decryptPassword(enpasswd,fmwVersion,domainName):
  if 'AES' in enpasswd:
    domain = "/opt/oracle/domains" + fmwVersion + "/" + domainName
    service = weblogic.security.internal.SerializedSystemIni.getEncryptionService(domain)
    encryption = weblogic.security.internal.encryption.ClearOrEncryptedService(service)
    return encryption.decrypt(enpasswd)
  else:
    errorMessage = "Encrypted password received is not of expected format"
    exitWithError(errorMessage)

#This function will connect to AdminServer
def adminConnect(user, passwd, adminHost, adminPort):
  try:
    connect(user, passwd, 't3://' + adminHost + ':' + adminPort)
  except:
    errorMessage = "Unable to connect to AdminServer"
    exitWithError(errorMessage)

def monitorJMS():
  import time
  servers = cmo.getServers()
  domainRuntime()

  for server in servers:
    serverName = server.getName()
    if serverName != "AdminServer":
      cd('/ServerRuntimes/' + serverName + '/JMSRuntime/' + serverName + '.jms')
      jmsServers = cmo.getJMSServers()
      for jmsServer in jmsServers:
        jmsServerName = jmsServer.getName()
        cd('/ServerRuntimes/' + serverName + '/JMSRuntime/' + serverName + '.jms' + '/JMSServers/' + jmsServerName)
        destinations = cmo.getDestinations()
        for destination in destinations:
          destinationName = destination.getName()
          if 'WLOSBJMSServer' in destinationName and 'ERRORQUEUE' not in destinationName:
            print destinationName + ":"
            print "--------------------------------------------------------------------"
            if "TOPIC" in destinationName:
              cd('/ServerRuntimes/' + serverName + '/JMSRuntime/' + serverName + '.jms' + '/JMSServers/' + jmsServerName + '/Destinations/' + destinationName)
              durableSubscribers = cmo.getDurableSubscribers()
              for durableSubscriber in durableSubscribers:
                durableSubscriberName = durableSubscriber.getName()
                print "  " + durableSubscriberName + ":"
                cd('/ServerRuntimes/' + serverName + '/JMSRuntime/' + serverName + '.jms' + '/JMSServers/' + jmsServerName + '/Destinations/' + destinationName + '/DurableSubscribers/' + durableSubscriberName)
                #print "    Currently active? " + str(cmo.getActive())
                print "    Last Message Received Time: " + str(time.strftime('%m-%d-%Y %H:%M:%S', time.gmtime(cmo.getLastMessagesReceivedTime()/1000.0)))
                print "    Messages Current Count: " + str(cmo.getMessagesCurrentCount())
                print "    Messages Pending Count: " + str(cmo.getMessagesPendingCount())
                print "    Subscribers Current Count: " + str(cmo.getSubscribersCurrentCount())
            elif "QUEUE" in destinationName:
              print "  Messages Current Count: " + str(cmo.getMessagesCurrentCount())
              print "  Messages Pending Count: " + str(cmo.getMessagesPendingCount())
            print "--------------------------------------------------------------------"
            print "\n"

def adminDisconnect():
  print "Disconnecting from AdminServer"
  disconnect()
  exit()

depasswd = decryptPassword(enpasswd,fmwVersion,domainName)
adminConnect('weblogic', depasswd, adminHost, adminPort)
monitorJMS()
adminDisconnect()
