####################################################################################################################################################
################This script has been prepared with an assumption that both AdminServer and ManagedServers are running from same host################
#########################################Run script in below format. Ensure to take wlst.sh from <SOA_HOME>#########################################
######<wlst.sh full path> retireNonDefaultComposites.py <admin-host> <admin-port> <console-username> <console-password> <managed-server-port>#######
####################################################################################################################################################
##################################This script can be extended further to undeploy composites that are non-default###################################

import os

compFile = "/home/oracle/deployedComposites.csv"

def validateCommandLineVars(argsCount):
  if argsCount != 6:
    print "Invalid usage of script. Read script description for the details."

#Remove compFile if it exists already
def removeCompfile(compFile):
  try:
    os.remove(compFile)
  except:
    print compFile + " is not found"
    pass

#Connect to AdminServer
def adminConnect(user, passwd, adminHost, adminPort):
  try:
    connect(user, passwd, 't3://' + adminHost + ':' + adminPort)
  except:
    print "Unable to connect to AdminServer"
    exit()

def retireNDComposites(compFile, adminHost, msPort, user, passwd):
  #Connect to managed server and write sca_listDeployedComposites output to /home/oracle/deployedComposites.csv
  old_stdout = sys.stdout
  sys.stdout = open(compFile, 'w')
  sca_listDeployedComposites(adminHost, msPort, user , passwd)
  sys.stdout = old_stdout

  #Read data from /home/oracle/deployedComposites.csv to identify isDefault=false composites
  f = open(compFile, 'r')
  composites = f.readlines()
  f.close()

  count = 0
  for composite in composites:
    if "isDefault=false" in composite :
      print composite
      print "---------------------------------------------------------"

      compName = composite.split(',')[0].split(' ')[1].split('[')[0]
      compVer = composite.split(',')[0].split(' ')[1].split('[')[1].split(']')[0]
      compPart = composite.split(',')[1].split('=')[1]
      print compName, compVer, compPart

      print "Retiring " + compName
      sca_retireComposite(adminHost, msPort, user, passwd, compName, compVer, partition=compPart)

      print "\nStopping " + compName
      sca_stopComposite(adminHost, msPort, user, passwd, compName, compVer, partition=compPart)

      print "---------------------------------------------------------"

      count = count + 1

  #No. of non-default composites
  print "No.of non-default composites: " + str(count)

validateCommandLineVars(len(sys.argv))
adminHost = sys.argv[1]
adminPort = sys.argv[2]
user = sys.argv[3]
passwd = sys.argv[4]
msPort = sys.argv[5]
removeCompfile(compFile)
adminConnect(user, passwd, adminHost, adminPort)
retireNDComposites(compFile, adminHost, msPort, user, passwd)
