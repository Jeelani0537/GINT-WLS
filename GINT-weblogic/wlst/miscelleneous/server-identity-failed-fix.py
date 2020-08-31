#############################################################################################
#Prepared by: Praveen Raj Kumar Kandregula
#Purpose: This has been prepared to fix "ServerIdentity failed validation, downgrading to 
#         anonymous"  errors
#############################################################################################

import sys
import commons
import wlstModule as wlm

host = sys.argv[1]
port = sys.argv[2]

def updateTrustPassword(domainName):
  from java.io import FileInputStream
  try:
    propInputStream = FileInputStream("/opt/oracle/scripts/.credentials.properties")
    configProps = Properties()
    configProps.load(propInputStream)
  except:
    errorMessage = "Error while reading properties"
    exitWithError(errorMessage)

  trustPassword = configProps.get("trustPassword")

  wlm.cd('/SecurityConfiguration/' + domainName)
  wlm.cmo.setCredential(trustPassword)
  print "Trust Password has been changed successfully"

user,passwd = commons.readCredentials()
commons.adminConnect(user, passwd, host, port)
domainName = wlm.cmo.getName()

commons.takeSession()

updateTrustPassword(domainName)

commons.activateChanges()
commons.disconnectWithSuccess()
commons.exitWithSuccess()
