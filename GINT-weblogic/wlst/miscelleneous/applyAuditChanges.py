#Ensure to source boot.properties from AdminServer/security before running this script.Run script in below format
#wlst.sh applyAuditChanges.py enpasswd domainName fmwVersion adminHost adminPort

import sys
import commons
import wlstModule as wlm

adminHost = sys.argv[1]
adminPort = sys.argv[2]
stack = sys.argv[6]

def applyAuditChanges():
  wlm.cd('/Servers/AdminServer/Log/AdminServer')
  wlm.cmo.setStdoutSeverity('Debug')
  print "Standard out logging has been changed to debug\n"
  
  wlm.cd('/Servers/AdminServer/ServerDebug/AdminServer')
  wlm.cmo.setDebugSecurityAtn(true)
  print "Security atn debug has been enabled\n"
  
  wlm.cd('/')
  wlm.cmo.setConfigurationAuditType('log')
  print "Configuration audit type has been changed to log\n"
  
  wlm.cd('/Servers/AdminServer/WebServer/AdminServer/WebServerLog/AdminServer')
  wlm.cmo.setELFFields('c-ip s-ip cs-username date time cs-method ctx-ecid ctx-rid cs-uri sc-status bytes cs(Referer) cs(UserAgent)')
  print "http logging format has been changed to: c-ip s-ip cs-username date time cs-method ctx-ecid ctx-rid cs-uri sc-status bytes cs(Referer) cs(UserAgent)\n"

if stack != "osbgtw":
  print "This is only applicable for OSB"
  commons.exitWithSuccess()

user,passwd = commons.readCredentials()
commons.adminConnect(user, passwd, adminHost, adminPort)

commons.takeSession()

applyAuditChanges()

commons.activateChanges()
commons.disconnectWithSuccess()
commons.exitWithSuccess()
