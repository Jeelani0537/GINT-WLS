#############################################################################################
#Prepared by: Praveen Raj Kumar Kandregula
#Purpose: This has been prepared as part of 11G/12C-patches-jul-2019 baseline. This script
#         updates CDS-ServiceAccounts and CDS-Users providers as per latest baseline.
#############################################################################################

import sys
import commons
import wlstModule as wlm

host = sys.argv[1]
port = sys.argv[2]
activity = sys.argv[5]

#Apply properties
applyProps = {
              'ServiceAccounts': {
                                  'AllUsersFilter': '(&(ikeastatus=ACTIVE)(ikeapersontype=3))',
                                  'UserFromNameFilter': '(&(uid=%u)(ikeastatus=ACTIVE)(ikeapersontype=3))',
                                  'UserBaseDN': 'ou=serviceaccounts,ou=global,o=ikea.com',
				  'UserObjectClass': 'ikeaperson'
               		         },
	      'Users':           {
                                  'AllUsersFilter': '(&(ikearolelist=its.oitp)(ikeastatus=ACTIVE)(objectclass=ikeaperson))',
                                  'UserFromNameFilter': '(&(ikealegacyuid=%u)(ikearolelist=its.oitp)(ikeastatus=ACTIVE)(objectclass=ikeaperson))'
	                         },
	      'Common':          {
                                  'GroupFromNameFilter': '(&(cn=%g)(objectclass=ikeausergroup))',
	                          'StaticGroupObjectClass': 'ikeausergroup',
	      	                  'StaticGroupDNsfromMemberDNFilter': '(&(uniquemember=%M)(objectclass=ikeausergroup))',
			          'GroupFromUserFilterForMemberuid': '(&(memberuid=%M)(objectclass=ikeausergroup))'
			         }
	     }

#Revert properties
revertProps = {
               'ServiceAccounts': {
                                   'AllUsersFilter': '(&(uid=*)(&(ikeastatus=ACTIVE)(objectclass=person)(|(ikeapersontype=3)(ikeaaccounttype=mac)(ikeaaccounttype=grp)(ikeaaccounttype=edu))))',
                                   'UserFromNameFilter': '(&(uid=%u)(&(ikeastatus=ACTIVE)(objectclass=person)(|(ikeapersontype=3)(ikeaaccounttype=mac)(ikeaaccounttype=grp)(ikeaaccounttype=edu))))',
                                   'UserBaseDN': 'o=ikea.com',
				   'UserObjectClass': 'person'
               			  },
	       'Users':           {
                                   'AllUsersFilter': ' ',
                                   'UserFromNameFilter': '(&(ikealegacyuid=%u)(ikearolelist=its.oitp)(objectclass=ikeaperson))'
			          },
	       'Common':          {
                                   'GroupFromNameFilter': '(&(cn=%g)(objectclass=groupofuniquenames))',
			           'StaticGroupObjectClass': 'groupofuniquenames',
				   'StaticGroupDNsfromMemberDNFilter': '(&(uniquemember=%M)(objectclass=groupofuniquenames))',
				   'GroupFromUserFilterForMemberuid': '(&(memberuid=%M)(objectclass=groupofuniquenames))'
				  }
               } 

def validateCDSHost(domainName):
  wlm.cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm/AuthenticationProviders/CDS-ServiceAccounts')
  currentCDSSAHost = wlm.cmo.getHost()
  
  wlm.cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm/AuthenticationProviders/CDS-Users')
  currentCDSUHost = wlm.cmo.getHost()
  
  if ('cdsp' not in currentCDSSAHost and 'cdsresp' in currentCDSSAHost) or ('cdsp' not in currentCDSUHost and 'cdsresp' in currentCDSSAHost):
    errorMessage = "cdsp is not found in either CDS-ServiceAccounts or CDS-Users!!!"
    commons.exitWithError(errorMessage)
  else:
    print 'cdsp is found in both the providers. Proceeding further!!!'

def loadProps(activity):
  if activity == 'apply':
    return applyProps
  elif activity == 'revert' :
    return revertProps

def applyCDSChanges(domainName,wlVersion,properties):
  wlm.cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm/AuthenticationProviders/CDS-ServiceAccounts')
  print '\nUpdating CDS-ServiceAccounts specific parameters'
  
  #wlm.cmo.setAllUsersFilter('(&(ikeastatus=ACTIVE)(ikeapersontype=3))')
  wlm.cmo.setAllUsersFilter(properties['ServiceAccounts']['AllUsersFilter'])
  print 'AllUsersFilter has been set to ' + properties['ServiceAccounts']['AllUsersFilter'] + ' for CDS-ServiceAccounts'
  
  #wlm.cmo.setUserFromNameFilter('(&(uid=%u)(ikeastatus=ACTIVE)(ikeapersontype=3))')
  wlm.cmo.setUserFromNameFilter(properties['ServiceAccounts']['UserFromNameFilter'])
  print 'UserFromNameFilter has been set to ' + properties['ServiceAccounts']['UserFromNameFilter'] + ' for CDS-ServiceAccounts'

  #wlm.cmo.setUserBaseDN('ou=serviceaccounts,ou=global,o=ikea.com')
  wlm.cmo.setUserBaseDN(properties['ServiceAccounts']['UserBaseDN'])
  print 'UserBaseDN has been set to: ' + properties['ServiceAccounts']['UserBaseDN']

  #wlm.cmo.setUserObjectClass('ikeaperson')
  wlm.cmo.setUserObjectClass(properties['ServiceAccounts']['UserObjectClass'])
  print 'UserObjectClass has been set to: ' + properties['ServiceAccounts']['UserObjectClass']
  
  wlm.cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm/AuthenticationProviders/CDS-Users')
  print '\nUpdating CDS-Users specific parameters'
  
  #wlm.cmo.setAllUsersFilter('(&(ikearolelist=its.oitp)(ikeastatus=ACTIVE)(objectclass=ikeaperson))')
  wlm.cmo.setAllUsersFilter(properties['Users']['AllUsersFilter'])
  print 'AllUsersFilter has been set to ' + properties['Users']['AllUsersFilter'] + ' for CDS-Users'
  
  #wlm.cmo.setUserFromNameFilter('(&(ikealegacyuid=%u)(ikearolelist=its.oitp)(ikeastatus=ACTIVE)(objectclass=ikeaperson))')
  wlm.cmo.setUserFromNameFilter(properties['Users']['UserFromNameFilter'])
  print 'UserFromNameFilter has been set to ' + properties['Users']['UserFromNameFilter'] + ' for CDS-Users'
  
  for provider in ['CDS-ServiceAccounts', 'CDS-Users']:
    print '\nUpdating common parameters for ' + provider
    wlm.cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm/AuthenticationProviders/' + provider)
	
    #wlm.cmo.setGroupFromNameFilter('(&(cn=%g)(objectclass=ikeausergroup))')
    wlm.cmo.setGroupFromNameFilter(properties['Common']['GroupFromNameFilter'])
    print 'GroupFromNameFilter has been set to ' + properties['Common']['GroupFromNameFilter'] + ' for ' + provider
	
    #wlm.cmo.setStaticGroupObjectClass('ikeausergroup')
    wlm.cmo.setStaticGroupObjectClass(properties['Common']['StaticGroupObjectClass'])
    print 'StaticGroupObjectClass has been set to ' + properties['Common']['StaticGroupObjectClass'] + ' for ' + provider
	
    #wlm.cmo.setStaticGroupDNsfromMemberDNFilter('(&(uniquemember=%M)(objectclass=ikeausergroup))')
    wlm.cmo.setStaticGroupDNsfromMemberDNFilter(properties['Common']['StaticGroupDNsfromMemberDNFilter'])
    print 'StaticGroupDNsfromMemberDNFilter has been set to ' + properties['Common']['StaticGroupDNsfromMemberDNFilter'] + ' for ' + provider
	
    if '10.3' not in wlVersion:
      #wlm.cmo.setGroupFromUserFilterForMemberuid('(&(memberuid=%M)(objectclass=ikeausergroup))')
      wlm.cmo.setGroupFromUserFilterForMemberuid(properties['Common']['GroupFromUserFilterForMemberuid'])
      print 'GroupFromUserFilterForMemberuid has been set to ' + properties['Common']['GroupFromUserFilterForMemberuid'] + ' for ' + provider

user,passwd = commons.readCredentials()
commons.adminConnect(user, passwd, host, port)

domainName = wlm.cmo.getName()
wlVersion = wlm.cmo.getConfigurationVersion()

validateCDSHost(domainName)
properties = loadProps(activity)
commons.takeSession()

try:
  applyCDSChanges(domainName,wlVersion,properties)
except: 
  errorMessage = "Unable to apply CDS changes!!!"
  commons.exitWithError(errorMessage)

commons.activateChanges()
commons.disconnectWithSuccess()
commons.exitWithSuccess()
