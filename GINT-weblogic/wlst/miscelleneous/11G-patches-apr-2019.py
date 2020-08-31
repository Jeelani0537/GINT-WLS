#Ensure to source boot.properties from AdminServer/security before running this script.Run script in below format
#wlst.sh healthCheck.py enpasswd domainName fmwVersion adminHost adminPort
import sys
enpasswd = sys.argv[1]
domainName = sys.argv[2]
fmwVersion = sys.argv[3]
adminHost = sys.argv[4]
adminPort = sys.argv[5]
def exitWithError(errorMessage):
  print "Script execution failed !!!" + errorMessage
  exit()
def decryptPassword(enpasswd,fmwVersion,domainName):
  if 'AES' in enpasswd:
    domain = "/opt/oracle/domains" + fmwVersion + "/" + domainName
    service = weblogic.security.internal.SerializedSystemIni.getEncryptionService(domain)
    encryption = weblogic.security.internal.encryption.ClearOrEncryptedService(service)
    return encryption.decrypt(enpasswd)
  else:
    #errorMessage = "Encrypted password received is not of expected format"
    #exitWithError(errorMessage)
    return enpasswd
def adminConnect(user, passwd, adminHost, adminPort):
  try:
    connect(user, passwd, 't3://' + adminHost + ':' + adminPort)
  except:
    errorMessage = "Unable to connect to AdminServer"
    exitWithError(errorMessage)
def baselineChanges():
  servers = cmo.getServers()
  #refinedProps = ""
  for server in servers:
    refinedProps = ""
    serverName = server.getName()
    if serverName == "AdminServer" :
      properties = "-Dweblogic.management.disableManagedServerNotifications=true -Dweblogic.ResolveDNSName=true -Dweblogic.MaxMessageSize=16000000"
    else:
      properties = "-Dweblogic.MaxMessageSize=16000000"
    cd('/Servers/' + serverName + '/ServerStart/' + serverName)
    currentProps = cmo.getArguments()
    print "In " + serverName + " tree.."
    if currentProps != "" and currentProps != None:
      print "Current properties: " + str(currentProps)
      for prop in properties.split(' '):
        if currentProps.find(prop) != -1 :
          print prop + " exists already"
        else:
          refinedProps = refinedProps + " " + prop
      updateProps = currentProps + " " + refinedProps
    else:
      updateProps = refinedProps
    print str(currentProps) + " will be updated with \n" + updateProps
    cmo.setArguments(updateProps)
    save()
    print "\n\n"
depasswd = decryptPassword(enpasswd,fmwVersion,domainName)
adminConnect('weblogic', depasswd, adminHost, adminPort)
try:
  edit()
  startEdit()
except:
  errorMessage = "Unable to take session. See if there are ny open sessions"
  exitWithError(errorMessage)

try:  
  baselineChanges()
except:
  errorMessage = "Error while applying baseline changes"
  exitWithError(errorMessage)

validate()
activate()
disconnect()
exit()
