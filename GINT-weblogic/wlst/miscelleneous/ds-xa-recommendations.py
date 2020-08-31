##Run script in below format##
#wlst.sh <script.py> <user> <password> <adminHost> <adminPort>
user = sys.argv[1]
passwd = sys.argv[2]
adminHost = sys.argv[3]
adminPort = sys.argv[4]

connect(user, passwd, 't3://' + adminHost + ':' + adminPort)
dataSources = cmo.getJDBCSystemResources()

for dataSource in dataSources:
  dataSourceName = dataSource.getName()
  #if dataSourceName not in ['EDNDataSource','EDNLocalTxDataSource','SOADataSource','SOALocalTxDataSource','OraSDPMDataSource','mds-soa','mds-owsm']:
  #if dataSourceName not in ['OraSDPMDataSource','SoaLeasingDataSource','SOADataSource','opss-data-source','EDNDataSource','opss-audit-viewDS','OITP_JMS_DS','mds-owsm','SOALocalTxDataSource','WLSSchemaDataSource','opss-audit-DBDS','EDNLocalTxDataSource','OITP_TLOG_DS','OITP_GENERIC_DS','LocalSvcTblDataSource','mds-soa']:
  print "------------------------------------------------------------------------------"
  print "Current datasource: " + dataSourceName

  cd('/JDBCSystemResources/' + dataSourceName + '/JDBCResource/' + dataSourceName + '/JDBCDriverParams/' + dataSourceName)
  driverType = cmo.getDriverName()

  if driverType == 'oracle.jdbc.xa.client.OracleXADataSource':
    print dataSourceName + " is xa datasource"

    try:
      edit()
      startEdit()
    except:
      errorMessage = "Unable to take session. See if there are ny open sessions"
      exitWithError(errorMessage)

    cd('/JDBCSystemResources/' + dataSourceName + '/JDBCResource/' + dataSourceName + '/JDBCDriverParams/' + dataSourceName + '/Properties/' + dataSourceName)
  
    if not getMBean('/JDBCSystemResources/' + dataSourceName + '/JDBCResource/' + dataSourceName + '/JDBCDriverParams/' + dataSourceName + '/Properties/' + dataSourceName + '/Properties/oracle.net.CONNECT_TIMEOUT'):
      print "oracle.net.CONNECT_TIMEOUT property doesn't exist. Creating now"
      cmo.createProperty('oracle.net.CONNECT_TIMEOUT')
    else:
      print "oracle.net.CONNECT_TIMEOUT property exists."

    cd('/JDBCSystemResources/' + dataSourceName + '/JDBCResource/' + dataSourceName + '/JDBCDriverParams/' + dataSourceName + '/Properties/' + dataSourceName + '/Properties/oracle.net.CONNECT_TIMEOUT')
    cmo.setValue('10000')

    cd('/JDBCSystemResources/' + dataSourceName + '/JDBCResource/' + dataSourceName + '/JDBCConnectionPoolParams/' + dataSourceName)
    print "Current ConnectionCreationRetryFrequencySeconds: " + str(cmo.getConnectionCreationRetryFrequencySeconds())
    cmo.setConnectionCreationRetryFrequencySeconds(10)
    print "ConnectionCreationRetryFrequencySeconds has been set to: " + str(cmo.getConnectionCreationRetryFrequencySeconds())

    cmo.setTestTableName('SQL SELECT 1 FROM DUAL\r\n')
    print "Test table name has been set to: SQL SELECT 1 FROM DUAL" 

    print "Current SecondsToTrustAnIdlePoolConnection: " + str(cmo.getSecondsToTrustAnIdlePoolConnection())
    cmo.setSecondsToTrustAnIdlePoolConnection(0)
    print "SecondsToTrustAnIdlePoolConnection has been set to: " + str(cmo.getConnectionCreationRetryFrequencySeconds())

    #print "Current TestConnectionsOnReserve: " + str(cmo.getTestConnectionsOnReserve())
    cmo.setTestConnectionsOnReserve(true)
    #print "TestConnectionsOnReserve has been set to: " + str(cmo.getTestConnectionsOnReserve())

    print "Current TestFrequencySeconds: " + str(cmo.getTestFrequencySeconds())
    cmo.setTestFrequencySeconds(300)
    print "TestFrequencySeconds has been set to: " + str(cmo.getTestFrequencySeconds())

    cd('/JDBCSystemResources/' + dataSourceName + '/JDBCResource/' + dataSourceName + '/JDBCXAParams/' + dataSourceName)
    #print "Current XaSetTransactionTimeout: " + str(cmo.getXaSetTransactionTimeout())
    cmo.setXaSetTransactionTimeout(true)

    #print "XaSetTransactionTimeout has been set to: " + str(cmo.getXaSetTransactionTimeout())
    print "Current XaRetryDurationSeconds: " + str(cmo.getXaRetryDurationSeconds())
    cmo.setXaRetryDurationSeconds(300)
    print "XaRetryDurationSeconds has been set to :" + str(cmo.getXaRetryDurationSeconds())

    validate()
    save()
  else:
    print dataSourceName + " is a non-xa datasource"
  print "------------------------------------------------------------------------------\n\n"

activate()
disconnect()
exit()
