import sys
import commons
import wlstModule as wlm

adminHost = sys.argv[1]
adminPort = sys.argv[2]
domainName = sys.argv[9]
fmwVersion = sys.argv[7]
#enpasswd = sys.argv[5]

users = ['ansibleuser', 'deployuser', 'oemsuperuser', 'bamuser']

def decryptPassword(fmwVersion,domainName):
  from java.io import FileInputStream
  try:
    propInputStream = FileInputStream("/opt/oracle/domains" + fmwVersion + "/" + domainName + "/boot.properties")
    configProps = Properties()
    configProps.load(propInputStream)
  except:
    errorMessage = "Error while reading properties"
    commons.exitWithError(errorMessage)

  enpasswd = configProps.get("password")

  if 'AES' in enpasswd:
    domain = "/opt/oracle/domains" + fmwVersion + "/" + domainName
    service = weblogic.security.internal.SerializedSystemIni.getEncryptionService(domain)
    encryption = weblogic.security.internal.encryption.ClearOrEncryptedService(service)
    return encryption.decrypt(enpasswd)
  else:
    #errorMessage = "Encrypted password received is not of expected format"
    #commons.exitWithError(errorMessage)
    return enpasswd

def createUsers(users, domainName):
  for user in users:
    print "Reading password from properties"

    from java.io import FileInputStream
    try:
      propInputStream = FileInputStream("/opt/oracle/scripts/.credentials.properties")
      configProps = Properties()
      configProps.load(propInputStream)
    except:
      errorMessage = "Error while reading properties"
      commons.exitWithError(errorMessage)

    password = configProps.get(user + "_password")
    #print password

    wlm.cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm/AuthenticationProviders/DefaultAuthenticator')

    if not wlm.cmo.userExists(user):
      wlm.cmo.createUser(user, password, 'Created via WLST from Ansible')
      print user + " has been created"
    wlm.cmo.addMemberToGroup('Administrators', user)
    print user + " has been added to Administrators"

depasswd = decryptPassword(fmwVersion,domainName)
commons.adminConnect('weblogic', depasswd, adminHost, adminPort)

createUsers(users, domainName)

commons.disconnectWithSuccess()
commons.exitWithSuccess()

