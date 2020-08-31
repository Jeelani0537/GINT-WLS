#############################################################################################
#Prepared by: Praveen Raj Kumar Kandregula
#Purpose: This will have re-usable methods of wlst. 
#############################################################################################
from wlstModule import *

def exitWithError(errorMessage):
  print "Script execution failed !!!" + errorMessage
  exit('y',1)

def readCredentials():
  from java.io import FileInputStream

  try:
    propInputStream = FileInputStream("/opt/oracle/scripts/.credentials.properties")
    configProps = Properties()
    configProps.load(propInputStream)
  except:
    errorMessage = "Error while reading properties"
    exitWithError(errorMessage)

  user = configProps.get("username")
  passwd = configProps.get("password")
  #bamPasswd = configProps.get("bam_password") 
  print "Credentials have been read successfully!!!"
  
  return user,passwd

def readBamPassword():
  from java.io import FileInputStream
  
  try:
    propInputStream = FileInputStream("/opt/oracle/scripts/.credentials.properties")
    configProps = Properties()
    configProps.load(propInputStream)
  except:
    errorMessage = "Error while reading properties"
    exitWithError(errorMessage)
 
  bamPasswd = configProps.get("bamuser_password")
  print "BAM password has been read successfully"

  return bamPasswd

def adminConnect(user, passwd, adminHost, adminPort):
  try:
    connect(user, passwd, 't3://' + adminHost + ':' + adminPort)
  except:
    errorMessage = "Unable to connect to server"
    exitWithError(errorMessage)
  
  print "Connected to server successfully!!!"

def takeSession():
  try:
    edit()
    startEdit()
  except:
    errorMessage = "Unable to take session!!!"
    exitWithError(errorMessage)

def activateChanges():
  try:
    save()
    activate()
  except:
    errorMessage = "Unable to save and activate!!!"
    exitWithError(errorMessage)

def disconnectWithSuccess():
  print "Script has been executed successfully. Disconnecting...!!!"
  disconnect()

def exitWithSuccess():
  exit()
