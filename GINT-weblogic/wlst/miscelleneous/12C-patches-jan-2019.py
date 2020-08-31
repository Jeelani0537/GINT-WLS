#############################################################################################
#Prepared by: Praveen Raj Kumar Kandregula
#Usage: wlst.sh healthCheck.py enpasswd domainName fmwVersion adminHost adminPort
#Purpose: This has been prepared as part of 12C-patches-jan-2019 baseline.
#############################################################################################

import sys
import commons
import wlstModule as wlm

host = sys.argv[1]
port = sys.argv[2]

def baselineChanges():
  servers = wlm.cmo.getServers()
  migratableTargets = wlm.cmo.getMigratableTargets()

  domainName = wlm.cmo.getName()
  wlm.cd('/JTA/' + domainName)
  wlm.cmo.setTimeoutSeconds(630)
  print "JTA TimeoutSeconds has been set to: 630"

  for server in servers:
    serverName = server.getName()
    print "In " + serverName + " tree"

    wlm.cd('/Servers/' + serverName + '/WebServer/' + serverName + '/WebServerLog/' + serverName)
    wlm.cmo.setELFFields('date time cs-method ctx-ecid ctx-rid cs-uri sc-status time-taken bytes')
    print "ELFFields have been set to: date time cs-method ctx-ecid ctx-rid cs-uri sc-status time-taken byte"

    wlm.cd('/Servers/' + serverName + '/Log/' + serverName)
    wlm.cmo.setFileMinSize(100000)
    print "Logs FileMinSize has been set to: 100000"

    wlm.cmo.setFileCount(50)
    print "Logs FileCount has been set to: 50"

  for migratableTarget in migratableTargets:
    migratableTargetName = migratableTarget.getName()
    wlm.cd('/MigratableTargets/' + migratableTargetName)
    wlm.cmo.setMigrationPolicy('manual')
    print migratableTargetName + " migration policy has been set to: manual"

user,passwd = commons.readCredentials()
commons.adminConnect(user, passwd, host, port)
commons.takeSession()

try:
  baselineChanges()
except:
  errorMessage = "Error while running baseline changes script"
  commons.exitWithError(errorMessage)

commons.activateChanges()
commons.disconnectWithSuccess()
commons.exitWithSuccess()
