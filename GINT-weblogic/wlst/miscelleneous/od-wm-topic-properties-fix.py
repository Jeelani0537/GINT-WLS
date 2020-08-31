#Prepared by:   Praveen Raj Kumar Kandregula
#Purpose:       This will help us update the properties mentioned at the start of the script at all topics of od and wm jms modules

import sys
import commons
import wlstModule as wlm

adminHost = sys.argv[1]
adminPort = sys.argv[2]

redeliveryDelayOverride = 10000
redeliveryLimit = 3
expirationPolicy = 'Redirect'
jmsModules = ['od', 'wm']

def updateTopicProperties(jmsModules, redeliveryDelayOverride, redeliveryLimit, expirationPolicy):
  for module in jmsModules:
    wlm.cd('/JMSSystemResources/' + module + '/JMSResource/' + module)
    print "In " + module
    topics = wlm.cmo.getUniformDistributedTopics()

    if len(topics) > 0:
      for topic in topics:
        topicName = topic.getName()
        errorQueue = topicName.replace("TOPIC", "ERRORQUEUE")

        wlm.cd('/JMSSystemResources/' + module + '/JMSResource/' + module + '/UniformDistributedTopics/' + topicName)
        print "  In " + topicName + "..."

        wlm.cd('/JMSSystemResources/' + module + '/JMSResource/' + module + '/UniformDistributedTopics/' + topicName + '/DeliveryParamsOverrides/' + topicName)
        wlm.cmo.setRedeliveryDelay(int(redeliveryDelayOverride))
        print "    RedeliveryDelayOverride " + str(redeliveryDelayOverride) + " has been set"

        wlm.cd('/JMSSystemResources/' + module + '/JMSResource/' + module + '/UniformDistributedTopics/' + topicName + '/DeliveryFailureParams/' + topicName)
        wlm.cmo.setRedeliveryLimit(int(redeliveryLimit))
        print "    RedeliveryLimit " + str(redeliveryLimit) + " has been set"

        wlm.cmo.setExpirationPolicy(expirationPolicy)
        print "    ExpirationPolicy " + expirationPolicy + " has been set"

        wlm.cmo.setErrorDestination(wlm.getMBean('/JMSSystemResources/' + module + '/JMSResource/' + module + '/UniformDistributedQueues/' + errorQueue))
        print "    ErrorDestination " + errorQueue + " has been set"

        print "\n"
    print "\n"

user,passwd = commons.readCredentials()
commons.adminConnect(user, passwd, adminHost, adminPort)

commons.takeSession()
updateTopicProperties(jmsModules, redeliveryDelayOverride, redeliveryLimit, expirationPolicy)

commons.activateChanges()
commons.disconnectWithSuccess()
commons.exitWithSuccess()
