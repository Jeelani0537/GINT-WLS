import sys

enpasswd = sys.argv[1]
domainName = sys.argv[2]
fmwVersion = sys.argv[3]
adminHost = sys.argv[4]
adminPort = sys.argv[5]
newpwd = sys.argv[6]

def exitWithError(errorMessage):
  print "Script execution failed !!!" + errorMessage
  exit('y',1)
  
def decryptPassword(enpasswd,fmwVersion,domainName):
  if 'AES' in enpasswd:
    domain = "/opt/oracle/domains" + fmwVersion + "/" + domainName
    service = weblogic.security.internal.SerializedSystemIni.getEncryptionService(domain)
    encryption = weblogic.security.internal.encryption.ClearOrEncryptedService(service)
    return encryption.decrypt(enpasswd)
  else:
    return enpasswd
  #else:
    #errorMessage = "Encrypted password received is not of expected format"
    #exitWithError(errorMessage)
	
def adminConnect(user, passwd, adminHost, adminPort):
  try:
    connect(user, passwd, 't3://' + adminHost + ':' + adminPort)
  except:
    errorMessage = "Unable to connect to AdminServer"
    exitWithError(errorMessage)
	
def resetPassword(new_passwd,domainName):
  try:
    #cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm/UserLockoutManager/UserLockoutManager')
    #cmo.setLockoutEnabled(false)
    #print "\n"
    #print "Disabled user lockout"

    cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm/AuthenticationProviders/DefaultAuthenticator')
    cmo.resetUserPassword("weblogic",new_passwd)
    print "weblogic user password has been reset"
  except:
    errorMessage = "Error while resetPassword."
    exitWithError(errorMessage)

  try:
    edit()
    startEdit()
  except:
    errorMessage = "Unable to take session. See if there are ny open sessions"
    exitWithError(errorMessage)

  cd('/EmbeddedLDAP/' + domainName)
  cmo.setRefreshReplicaAtStartup(true)
  #cmo.setMasterFirst(true)
  print "LDAP level changes have been done"
  
  cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm/UserLockoutManager/UserLockoutManager')
  cmo.setLockoutEnabled(false)
  print "\n"
  print "Disabled user lockout"


  save()
  validate()
  activate()

depasswd = decryptPassword(enpasswd,fmwVersion,domainName)
adminConnect('weblogic', depasswd, adminHost, adminPort)

resetPassword(newpwd,domainName)

disconnect()
exit()
