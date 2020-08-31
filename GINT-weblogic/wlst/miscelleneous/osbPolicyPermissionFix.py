#############################################################################################
#Prepared by: Praveen Raj Kumar Kandregula
#Purpose: This will add principle 'AdminOnlyTaskAccess' to 'MiddlewareAdministrator' to avoid
#         permission issues while attaching a policy to a OSB service
#Doc ref: https://support.oracle.com/epmos/faces/DocumentDisplay?_afrLoop=512834771872846&id=1963087.1&displayIndex=1&_afrWindowMode=0&_adf.ctrl-state=hbgqq0i20_29
#############################################################################################
import sys
import commons

adminHost = sys.argv[1]
adminPort = sys.argv[2]

def addPrinicipleToRole():
  from StringIO import StringIO
  old_stdout = sys.stdout
  var = StringIO()
  sys.stdout = var

  listAppRoleMembers(appStripe="Service_Bus_Console", appRoleName="MiddlewareAdministrator")
  sys.stdout = old_stdout

  if 'AdminOnlyTaskAccess' in var.getvalue():
    print "Role:MiddlewareAdministrator already has the principle:AdminOnlyTaskAccess attached!!!"
  else:
    grantAppRole(appStripe="Service_Bus_Console", appRoleName="MiddlewareAdministrator", principalClass="oracle.soa.osb.console.common.permissions.OSBPermission", principalName="AdminOnlyTaskAccess")
    print "Principle:AdminOnlyTaskAccess has been attached to role:MiddlewareAdministrator successfully!!!"

user,passwd = commons.readCredentials()
commons.adminConnect(user, passwd, adminHost, adminPort)
addPrinicipleToRole()
commons.disconnectWithSuccess()
commons.exitWithSuccess()
