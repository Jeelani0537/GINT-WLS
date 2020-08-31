#Ensure to source boot.properties from AdminServer/security before running this script.Run script in below format
#wlst.sh dcdRecommendations.py enpasswd domainName fmwVersion adminHost adminPort

import sys

enpasswd = sys.argv[1]
domainName = sys.argv[2]
fmwVersion = sys.argv[3]
adminHost = sys.argv[4]
adminPort = sys.argv[5]

usersList = ['oemsuperuser', 'deployuser']
outputFile = "/tmp/user-status.txt"

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

def adminDisconnect():
  print "Disconnecting from AdminServer"
  disconnect()
  exit()

def validateUsers(domainName):
  cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm/AuthenticationProviders/DefaultAuthenticator')
  for user in usersList:
    userStatus = cmo.userExists(user)
    if userStatus == 0 :
      print user + " does not exist in " + domainName

depasswd = decryptPassword(enpasswd,fmwVersion,domainName)

adminConnect('weblogic', depasswd, adminHost, adminPort)

old_stdout = sys.stdout
sys.stdout = open(outputFile, 'w')
validateUsers(domainName)

sys.stdout = old_stdout
adminDisconnect()
