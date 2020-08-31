import sys
#Properties being passed to this script should be of this format. This format is bound to change as per the requirement later
keys = "Type(XA/Non-XA);Name;jndiName;dsType(Generic/GridLink/Multi);connectionString;userName;password;targets"
dictKeys = ["Type", "Name", "jndiName", "dsType", "connectionString", "userName", "password", "targets"]
dictResources = {}
scriptName = "createGenericXADataSources.py"
#Methods definition
def exitWithError(message):
  print message
  exit()
def adminConnect(user, passwd, adminHost, adminPort):
  try:
    connect(user, passwd, "t3://" + adminHost + ":" + adminPort)
    print "Successfully connected to AdminServer"
  except:
    message = "==>Unable to connect to admin server"
    exitWithError(message)
def createGenericXADataSources(dictResources):
  resType = dictResources['Type'].replace(" ","")
  dsName = dictResources['Name'].replace(" ","")
  jndiName = dictResources['jndiName'].replace(" ","")
  dsType = dictResources['dsType'].replace(" ","")
  connectionString = dictResources['connectionString'].replace(" ","")
  userName =  dictResources['userName'].replace(" ","")
  password = dictResources['password'].replace(" ","")
  targets = dictResources['targets'].replace(" ","")
  print "==============================================================================================="
  if resType == "NULL"  or dsName == "NULL" or jndiName == "NULL" or dsType == "NULL" or connectionString == "NULL" or userName == "NULL" or password =="NULL" or targets == "NULL":
    message = "Invalid values passed to create datasource. Validate the data in properties file and re-run"
    exitWithError(message)
  else:
    print "Variables validation is successful"
    if not getMBean('/JDBCSystemResources/' + dsName) and (resType == "XA" or resType == "Non-XA"):
      print dsName + " doesn't exist"
      print "Creating " + dsName
	  
      if resType == "XA" :
        driverName = "oracle.jdbc.xa.client.OracleXADataSource"
        transactionProtocol = "TwoPhaseCommit"
      else if resType == "Non-XA":
        driverName = "oracle.jdbc.OracleDriver"
        transactionProtocol = "OnePhaseCommit"
      try:		
        edit()
        startEdit()
      except:
        errorMessage = "Unable to take session. See if there are ny open sessions"
        exitWithError(errorMessage)
      
      cd('/')
      cmo.createJDBCSystemResource(dsName)
      cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName)
      cmo.setName(dsName)

      cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName)
      set('JNDINames',jarray.array([String(jndiName)], String))
      print "JNDIName has been set to " + jndiName

      cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName)
      cmo.setDatasourceType(dsType)
      print "Type has been set to " + dsType

      cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName)
      cmo.setUrl(connectionString)
      print "URL has been set to " + connectionString

      cmo.setDriverName(driverName)
      set('Password', password)

      cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName)
      cmo.createProperty('user')
      cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/user')
      cmo.setValue(userName)
      print "User has been set to " + userName

      cd('/JDBCSystemResources/' + dsName)
      set('Targets',jarray.array([ObjectName('com.bea:Name=' + targets + ',Type=Cluster')], ObjectName))
      print "Targets have been set to " + targets

      cd('/JDBCSystemResources/' + dsName ' + /JDBCResource/' + dsName ' + /JDBCDataSourceParams/' + dsName)
      cmo.setGlobalTransactionsProtocol(transactionProtocol)
      print "Transaction protocol has been set to: " + transactionProtocol

      if resType == "XA" :
	print "Configuring XA additional parameters..."

        cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName)
        cmo.createProperty('oracle.net.CONNECT_TIMEOUT')
        cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/oracle.net.CONNECT_TIMEOUT')
        cmo.setValue('10000')

        cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCConnectionPoolParams/' + dsName)
        cmo.setInitialCapacity(0)
        cmo.setTestConnectionsOnReserve(true)
        cmo.setTestTableName('SQL SELECT 1 FROM DUAL\r\n')
        cmo.setConnectionCreationRetryFrequencySeconds(10)
        cmo.setTestFrequencySeconds(300)
        cmo.setSecondsToTrustAnIdlePoolConnection(0)

        cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCXAParams/' + dsName)
        cmo.setXaTransactionTimeout(0)
        cmo.setXaSetTransactionTimeout(true)
        cmo.setKeepXaConnTillTxComplete(true)
        cmo.setXaRetryDurationSeconds(300)
        cmo.setXaRetryIntervalSeconds(60)

      validate()
      save()

    else:
      print dsName + " exists!!!"
  print "===============================================================================================\n\n"
#Reading properties file
try:
  propertiesFile = sys.argv[1]
  print "==>Properties file has been identified...\n\n"
except:
  message = "==>Invalid usage of script. Run the script in below format \n==><wlst.sh with full path> " + scriptName + " <resources properties file with full path> <console-username> <console-password> <admin-host> <admin-port>"
  exitWithError(message)
#Command line args validation
if len(sys.argv) != 6 :
  message = "==>Invalid usage of script. Run the script in below format \n==><wlst.sh with full path> " + scriptName + " <resources properties file with full path> <console-username> <console-password> <admin-host> <admin-port>"
  exitWithError(message)
else:
  #Reading command line variables
  user = sys.argv[2]
  passwd = sys.argv[3]
  adminHost = sys.argv[4]
  adminPort = sys.argv[5]
  #Read csv properties file
  f = open(propertiesFile)
  header = f.readline().lower()
  resources = f.readlines()
  if len(resources) == 0:
    message = "==>No resources found in properties file to be created"
    exitWithError(message)
  #Properties file header validation
  if header.replace("\n","") != keys.lower() :
    message = "==>Invalid header found in properties file"
    exitWithError(message)
  else:
    print "Header validation is successful"
    #Connect to admin server
    adminConnect(user, passwd, adminHost, adminPort)
    for resource in resources:
      resource = resource.replace("\n","")
      #if resource.endswith(","):
        #resource = resource + "NULL"
      #resource = resource.replace(",,",",NULL,")
      flag = 0
      for item in resource.split(";"):
        if item == "":
          item = "NULL"
        dictResources[dictKeys[flag]] = item
        flag = flag + 1
      #Call JMS Resource Creation method
      createGenericXADataSources(dictResources)

  activate()
  disconnect()
  exit()
